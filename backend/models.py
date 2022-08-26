from sqlalchemy import create_engine, Column, String, Integer, Float, Date, DateTime, LargeBinary, select, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import StaticPool
import datetime

# engine = create_engine('sqlite:///demo.db', echo=True, future=True)
# engine = create_engine('sqlite:///test1.db?charset=utf8', echo=True, future=True, )
# engine = create_engine('sqlite://', echo=True, future=True)
# engine = create_engine('sqlite://', future=True)
# engine = create_engine(
#     'sqlite://',
#     connect_args={'check_same_thread':False},
#     poolclass=StaticPool,
#     echo=True,
#     future=True)

engine = create_engine(
    'postgresql://leevi@localhost:5432/kulut_test',
    # connect_args={'check_same_thread':False},
    # poolclass=StaticPool,
    echo=True,
    future=True)

Session = sessionmaker(bind=engine, future=True)

Base = declarative_base()


class Submission(Base):
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
        return f'Submission(submission_id={self.submission_id}, name={self.name}, iban={self.iban}, submitted_at={self.submitted_at})'

    def as_dict(self):
        out = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        out['expenses'] = [exp.as_dict() for exp in self.expenses]
        out['allowances'] = [al.as_dict() for al in self.allowances]
        return out

    # @property
    # def allowance_value(self) -> float:
    #     return sum(allwoance.value for allwoance in self.allowances)

class Expense(Base):
    __tablename__ = 'expenses'
    expense_id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submissions.submission_id'))
    submission = relationship('Submission', back_populates='expenses')
    description = Column(String, nullable=False)
    receipt_filename = Column(String, nullable=False)
    receipt_data = Column(LargeBinary, nullable=False)
    value = Column(Float, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'receipt_data'}

    def __repr__(self) -> str:
        return f'Expense(id={self.expense_id}, submission_id={self.submission_id}, filename={self.receipt_filename}, value={self.value})'


class Allowance(Base):
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

    # @property
    # def value(self) -> float:
    #     return self.trip_length * self.per_km

    def __repr__(self) -> str:
        return f'Allowance(id={self.allowance_id}, submission_id={self.submission_id}, trip_length={self.trip_length})'

Base.metadata.create_all(engine)
