import flask
from kulumasiina_backend.models import Session, Submission, Expense, Allowance
from sqlalchemy import select, func, union
from werkzeug.formparser import FileStorage
import secrets
import datetime
import io
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt
from functools import wraps
import env


EXPENSE_PREFIX = 'expense-item-'
ALLOWANCE_PREFIX = 'allowance-item-'

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024**2
app.config['JSON_AS_ASCII'] = False


@app.get('/api/cheat')
def super_token():
    """
    Get a valid token without actually logging in.
    
    TODO: disble this before launch & invalidate old tokens by changing
    JWT secret to a new one.
    """
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
    return jwt.encode({'user': env.EMAILS[0], 'exp': exp_time}, env.SECRET)


def admin_only(f):
    """Decorator for checking issued JWT token validity."""
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = flask.request.headers.get('Authorization', None)
            if token is not None:
                token = token.removeprefix('Bearer ')
                decoded = jwt.decode(
                    token, env.SECRET, algorithms='HS256', require=['exp', 'user'])
                user = decoded['user']
                # exp_time = datetime.datetime.fromtimestamp(decoded['exp'])
                if user in env.EMAILS:
                    return f(*args, **kwargs)
        except:
            return '', 403
    return decorator


@app.post('/api/login')
def check_login():
    """Get a JWT token on successful login."""
    idinfo = id_token.verify_oauth2_token(
        flask.request.data,
        requests.Request(),
        env.GOOGLE_CLIENT_ID)
    if (email := idinfo['email']) in env.EMAILS:
        exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        return jwt.encode({'user': email, 'exp': exp_time}, env.SECRET)
    return '', 403


@app.get('/api/ping')
def pong():
    """Test if api is alive & routing works."""
    return '', 200


@app.get('/api/submissions')
@admin_only
def get_submissions():
    expense_stmt = (
        select(
            Submission.submission_id,
            func.sum(Expense.value).label('expense_sum'),
            func.count().label('expense_count'))
        .join(Expense)
        .group_by(Submission)
        .subquery()
    )
    allowance_value = Allowance.trip_length * Allowance.per_km
    allowance_stmt = (
        select(
            Submission.submission_id,
            func.sum(allowance_value).label('allowance_sum'),
            func.count().label('allowance_count')
        ).join(Allowance)
        .group_by(Submission)
        .subquery()
    )
    joined_stmt = (
        select(
            Submission.submission_id,
            Submission.name,
            Submission.submitted_at,
            Submission.accepted_meeting,
            Submission.accepted_at,
            Submission.paid_at,
            expense_stmt.c.expense_sum,
            expense_stmt.c.expense_count,
            allowance_stmt.c.allowance_sum,
            allowance_stmt.c.allowance_count)
        .join(
            expense_stmt,
            Submission.submission_id == expense_stmt.c.submission_id,
            isouter=True)
        .join(
            allowance_stmt,
            Submission.submission_id == allowance_stmt.c.submission_id,
            isouter=True)
        .order_by(
            Submission.paid_at,
            Submission.accepted_meeting,
            Submission.submitted_at.desc())
    )

    with Session() as session:
        rows = session.execute(joined_stmt).all()
    res = [dict(row) for row in rows]
    return res


@app.get('/api/submissions/<int:id>')
@admin_only
def get_submission(id: int):
    stmt = select(Submission).where(Submission.submission_id == id)
    with Session() as session:
        submission: Submission = session.execute(stmt).scalar_one()
        out = submission.as_dict()
    return out


@app.get('/api/file/<fname>')
@admin_only
def get_file(fname: str):
    stmt = (
        select(Expense.receipt_data)
        .where(Expense.receipt_filename == fname)
    )
    with Session() as session:
        res = session.execute(stmt).scalar_one()

    return flask.send_file(io.BytesIO(res), download_name=fname)


@app.post('/api/submit')
def handle_submit():
    save_submission(flask.request.form, flask.request.files)
    return '', 200


def parse_keys(data: dict[str, str]) -> tuple[set[str], set[str]]:
    """Parse item id sets for expenses and allowances from form data."""
    expense_keys = [k for k in data.keys() if k.startswith(EXPENSE_PREFIX)]
    allowance_keys = [k for k in data.keys() if k.startswith(ALLOWANCE_PREFIX)]
    expense_ids = set(
        key[len(EXPENSE_PREFIX):].split('-')[0] for key in expense_keys)
    allowance_ids = set(
        key[len(ALLOWANCE_PREFIX):].split('-')[0] for key in allowance_keys)
    return expense_ids, allowance_ids


def create_expenses(
        ids: set[str], 
        data: dict[str, str],
        files: dict[str, FileStorage]) -> list[Expense]:
    out: list[Expense] = []
    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
    while ids:
        i = ids.pop()
        description = data[f'expense-item-{i}-desc']
        value = data[f'expense-item-{i}-value']
        file = files[f'expense-item-{i}-receipt']
        fname = file.filename
        extension = fname.split('.')[-1].lower()
        if extension not in allowed_extensions:
            raise ValueError('Invalid file type')
        new_fname = f'{secrets.token_hex(8)}.{extension}'
        out.append(Expense(
            description=description,
            value=float(value),
            receipt_filename=new_fname,
            receipt_data=file.stream.read(),
        ))
    return out


def create_allowances(ids: set[str], data: dict[str, str]) -> list[Allowance]:
    out: list[Allowance] = []
    while ids:
        i = ids.pop()
        description = data[f'allowance-item-{i}-desc']
        # TODO: this is not used at all, remove from form
        value = data[f'allowance-item-{i}-value']
        kms = data[f'allowance-item-{i}-kms']
        out.append(Allowance(
            description=description,
            # TODO: include these in form
            route='ROUTE PLACEHOLDER',
            plate_no='PLATE-NO PLACEHOLDER',
            trip_length=float(kms),
            # TODO: per_km may change: fetch from some source based on date
            per_km=0.25
        ))
    return out


def save_submission(data: dict[str, str], files: dict[str, FileStorage]):
    """Cretate Submission, Expense, and Allowance entries from form data."""
    name = data['fullName']
    iban = data['iban']  # TODO: server-side form validation
    # TODO: parse social security number in case form has allowance requests
    expense_ids, allowance_ids = parse_keys(data)
    expenses = create_expenses(expense_ids, data, files)
    allowances = create_allowances(allowance_ids, data)
    submission = Submission(
        name=name,
        iban=iban,
        submitted_at=datetime.datetime.now(),
        expenses=expenses,
        allowances=allowances,
    )
    with Session() as session, session.begin():
        session.add(submission)
