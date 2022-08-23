import flask
import psycopg
import secrets
import io

conn_str = 'postgresql://leevi@localhost:5432/kulut'

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024**2


@app.post('/api/submit')
def handle_submit():
    data = flask.request.get_data()
    print(data)
    # try:
        # log_submit(flask.request.form)
    save_submission(flask.request.form, flask.request.files)
    # except Exception as e:
        # print(e)
        # return 'pieleen meni'
    return {'msg': 'ok'}

@app.get('/api/file/<fname>')
def serve_files(fname: str):
    print(fname)
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT receipt_file FROM submissions WHERE filename = %s', (fname,))
            res = cur.fetchone()
    if res is None:
        flask.abort(404)
    file_data = res[0]
    return flask.send_file(io.BytesIO(file_data), download_name=fname)

def log_submit(data: dict[str, str]):
    name = data['fullName']
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO logs (msg) values (%s)', (name,))
            conn.commit()

def parse_keys(data: dict[str, str]) -> tuple[set[str], set[str]]:
    expense_keys = [k for k in data.keys() if k.startswith('expense-item-')]
    allowance_keys = [k for k in data.keys() if k.startswith('allowance-item-')]
    expense_ids = set(key[13:].split('-')[0] for key in expense_keys)
    allowance_ids = set(key[15:].split('-')[0] for key in allowance_keys)
    return expense_ids, allowance_ids


EXPENSE_COMMAND = """INSERT INTO submissions (
    name,
    iban,
    description,
    is_expense,
    value,
    filename,
    receipt_file,
    received_at
) values (
    %s,%s, %s, true, %s, %s, %s, now()
);
"""

ALLOWANCE_COMMAND = """INSERT INTO submissions (
    name,
    iban,
    social_security,
    description,
    is_expense,
    value,
    kms,
    received_at
) values (
    %s, %s, %s, %s, false, %s, %s, now()
);
"""


def save_submission(data: dict[str, str], files):
    name = data['fullName']
    iban = data['iban']
    social_security = data.get('socialSecurity', None)
    # print(data.keys())
    exp_ids, allow_ids = parse_keys(data)
    extensions = ['pdf', 'jpg', 'jpeg', 'png']
    with psycopg.connect(conn_str) as conn:
        while exp_ids:
            i = exp_ids.pop()
            description = data[f'expense-item-{i}-desc']
            value = data[f'expense-item-{i}-value']
            file = files[f'expense-item-{i}-receipt']
            fname = file.filename
            extension = fname.split('.')[-1].lower()
            assert extension in extensions, 'Forbidden extension'
            file_data = file.read()
            new_fname = f'{secrets.token_hex(8)}.{extension}'
            with conn.cursor() as cur:
                cur.execute(
                    EXPENSE_COMMAND,
                    (
                        name,
                        iban,
                        description,
                        float(value),
                        new_fname,
                        file_data,
                    )
                )
        
        while allow_ids:
            i = allow_ids.pop()
            description = data[f'allowance-item-{i}-desc']
            value = data[f'allowance-item-{i}-value']
            kms = data[f'allowance-item-{i}-kms']
            with conn.cursor() as cur:
                cur.execute(
                    ALLOWANCE_COMMAND,
                    (
                        name,
                        iban,
                        social_security,
                        description,
                        float(value),
                        float(kms)
                    )
                )
        conn.commit()



@app.get('/api/logs')
def get_logs():
    with psycopg.connect('postgresql://leevi@localhost:5432/kulut') as conn:
        with conn.cursor() as cur:
            res = cur.execute('SELECT * FROM logs').fetchall()
            cols = cur.description
    return {'columns': [c[0] for c in cols], 'values': res}

def init_table():
    db_table = """CREATE TABLE submissions (
        id serial primary key,
        name text,
        iban text,
        social_security text,
        description text,
        is_expense bool,
        value real,
        kms real,
        filename text,
        receipt_file bytea,
        received_at timestamp,
        accepted_at timestamp,
        paid_at timestamp);
    """
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(db_table)
            conn.commit()