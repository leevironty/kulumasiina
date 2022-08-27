import flask
# import psycopg
from kulumasiina_backend.models import Session, Submission, Expense, Allowance
from sqlalchemy import select, func, union
from werkzeug.formparser import FileStorage
import secrets
import datetime
import io

# conn_str = 'postgresql://leevi@localhost:5432/kulut'

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024**2
app.config['JSON_AS_ASCII'] = False


@app.get('/<path:path>')
def serve_static(path):
    if '.' not in path:
        path = path + '.html'
    return flask.send_from_directory('../frontend/build', path)


@app.get('/')
def serve_base():
    return flask.send_from_directory('../frontend/build', 'index.html')


@app.get('/api/submissions')
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
    allowance_stmt = (
        select(
            Submission.submission_id,
            func.sum(Allowance.trip_length * Allowance.per_km).label('allowance_sum'),
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
            allowance_stmt.c.allowance_count,
        )
        .join(expense_stmt, Submission.submission_id == expense_stmt.c.submission_id, isouter=True)
        .join(allowance_stmt, Submission.submission_id == allowance_stmt.c.submission_id, isouter=True)
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
def get_one_submission(id: int):
    stmt = select(Submission).where(Submission.submission_id == id)
    with Session() as session:
        submission: Submission = session.execute(stmt).scalar_one()
        out = submission.as_dict()
    return out

@app.get('/api/file/<fname>')
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
    return {'msg': 'ok'}


def parse_keys(data: dict[str, str]) -> tuple[set[str], set[str]]:
    expense_keys = [k for k in data.keys() if k.startswith('expense-item-')]
    allowance_keys = [k for k in data.keys() if k.startswith('allowance-item-')]
    expense_ids = set(key[13:].split('-')[0] for key in expense_keys)
    allowance_ids = set(key[15:].split('-')[0] for key in allowance_keys)
    return expense_ids, allowance_ids


def generate_expenses(ids: set[str], data: dict[str, str], files: dict[str, FileStorage]) -> list[Expense]:
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


def generate_allowances(ids: set[str], data: dict[str, str]) -> list[Allowance]:
    out: list[Allowance] = []
    while ids:
        i = ids.pop()
        description = data[f'allowance-item-{i}-desc']
        value = data[f'allowance-item-{i}-value']
        kms = data[f'allowance-item-{i}-kms']
        out.append(Allowance(
            description=description,
            route='ROUTE PLACEHOLDER',
            plate_no='PLATE-NO PLACEHOLDER',
            trip_length=float(kms),
            per_km=0.25
        ))
    return out


def save_submission(data: dict[str, str], files: dict[str, FileStorage]):
    name = data['fullName']
    iban = data['iban']
    exp_ids, allow_ids = parse_keys(data)
    expenses = generate_expenses(exp_ids, data, files)
    allowances = generate_allowances(allow_ids, data)
    submission = Submission(
        name=name,
        iban=iban,
        submitted_at=datetime.datetime.now(),
        expenses=expenses,
        allowances=allowances,
    )
    with Session() as session, session.begin():
        session.add(submission)
