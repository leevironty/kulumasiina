from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    Float,
    DateTime,
    LargeBinary,
    ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import env


_engine = create_engine(env.CONN_STR, echo=True, future=True)
# Use this for creating DB sessions
Session = sessionmaker(bind=_engine, future=True)

Base = declarative_base()


class Submission(Base):
    """Model keeping data from a single submission together."""
    __tablename__ = 'submissions'
    submission_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    iban = Column(String, nullable=False)
    accepted_meeting = Column(String)
    submitted_at = Column(DateTime, nullable=False)
    accepted_at = Column(DateTime)
    paid_at = Column(DateTime)
    expenses = relationship('Expense', back_populates='submission')
    allowances = relationship('Allowance', back_populates='submission')

    def __repr__(self) -> str:
        return (
            f'Submission(submission_id={self.submission_id}, name={self.name}, '
            f'iban={self.iban}, submitted_at={self.submitted_at})'
        )

    def as_dict(self):
        out = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        out['expenses'] = [exp.as_dict() for exp in self.expenses]
        out['allowances'] = [al.as_dict() for al in self.allowances]
        return out


class Expense(Base):
    """Model for an expense reimbursement."""
    __tablename__ = 'expenses'
    expense_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.submission_id'))
    submission = relationship('Submission', back_populates='expenses')
    description = Column(String, nullable=False)
    receipt_filename = Column(String, nullable=False)
    receipt_data = Column(LargeBinary, nullable=False)
    value = Column(Float, nullable=False)

    def as_dict(self):
        return {
            c.name: getattr(self, c.name) for c in self.__table__.columns
            if c.name != 'receipt_data'
        }

    def __repr__(self) -> str:
        return (
            f'Expense(id={self.expense_id}, submission_id={self.submission_id},'
            f' filename={self.receipt_filename}, value={self.value})'
        )


class Allowance(Base):
    """Model for mileage / KM allowance."""
    __tablename__ = 'allowances'
    allowance_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.submission_id'))
    submission = relationship('Submission', back_populates='allowances')
    description = Column(String, nullable=False)
    route = Column(String, nullable=False)
    plate_no = Column(String, nullable=False)
    trip_length = Column(Float, nullable=False)
    per_km = Column(Float, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return (
            f'Allowance(id={self.allowance_id}, submission_id='
            f'{self.submission_id}, trip_length={self.trip_length})'
        )

# init DB schema if DB is empty (or models are missing)
Base.metadata.create_all(_engine)
