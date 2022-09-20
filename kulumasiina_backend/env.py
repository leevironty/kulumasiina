import os
from dotenv import load_dotenv

if 'JWT_SECRET' not in os.environ:
    load_dotenv('../.env.api')

SECRET = os.environ['JWT_SECRET']
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
EMAILS = os.environ['ADMIN_EMAILS'].replace(' ','').split(',')
CONN_STR = os.environ.get('CONN_STR', 'sqlite:///demo.db')
