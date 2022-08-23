import flask
import psycopg
import secrets

conn_str = 'postgresql://leevi@localhost:5432/kulut'

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024**2


@app.post('/api/submit')
def handle_submit():
    data = flask.request.get_data()
    print(data)
    try:
        # log_submit(flask.request.form)
        record_submit(flask.request.form, flask.request.files)
    except Exception as e:
        print(e)
        return 'pieleen meni'
    return {'msg': 'ok'}

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
    %s,%s, %s, %s, %s, %s, %s, now()
);
"""


def record_submit(data: dict[str, str], files):
    name = data['fullName']
    iban = data['iban']
    social_security = data.get('socialSecurity', None)
    print(files)
    print(data.keys())
    exp_ids, allow_ids = parse_keys(data)
    extensions = ['pdf', 'jpg', 'jpeg', 'png']
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
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    EXPENSE_COMMAND,
                    (
                        name,
                        iban,
                        description,
                        True,
                        float(value),
                        new_fname,
                        file_data,
                    ))
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