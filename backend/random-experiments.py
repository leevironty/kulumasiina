from models import Session, Submission, Expense, Allowance
from sqlalchemy import select, func
import json

# with Session() as session:
#     subs = select(Submission)
#     vals = select(
#         [
#             Allowance,
#             func.sum(Allowance.per_km * Allowance.trip_length)
#         ]
#     ).group_by(Allowance.submission_id)
#     stmt = subs.join(vals, Submission.allowances)

#     stmt = select(Submission).join(Expense, Submission.submission_id == Expense.submission_id).group_by()
#     res = session.execute(stmt).scalars().all()
#     # res = session.execute(vals).all()

#     print(type(res))
#     print(res[0])
#     # print([(r, r.allowance_value) for r in res])

with Session() as session:
    stmt = (
        select(
            Submission.submission_id,
            Submission.name,
            Submission.submitted_at,
            Submission.accepted_meeting,
            Submission.paid_at,
            func.sum(Allowance.trip_length * Allowance.per_km).label('allowance_sum'),
            func.sum(Expense.value).label('expense_sum'),
            func.count().label('item_count'))
        .join(Allowance, isouter=True)
        .join(Expense, isouter=True)
        .group_by(Submission)
        .order_by(
            Submission.submitted_at.desc(),
            Submission.accepted_meeting,
            Submission.paid_at)
    )
    res = session.execute(stmt).all()
    for r in res:
        print(dict(r))