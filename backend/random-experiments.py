from models import Session, Submission, Expense, Allowance
from sqlalchemy import select
import json

with Session() as session:
    stmt = select([Submission.name, Submission.iban])
    res = session.execute(stmt).all()

print(res)

stmt = select([Submission.name, Submission.iban])
with Session() as session:
    out = session.execute(stmt).all()

print(res)
print(type(res[0]))
print(dict(res[0]))
print(type(out))
print(json.dumps(out))