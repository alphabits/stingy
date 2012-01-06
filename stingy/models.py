from sqlalchemy import Column, Integer, String, Unicode, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from stingy.database import Base, Timestampable, DBModel


class User(Base, DBModel, Timestampable):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode)
    events = relationship('Event', backref='creator')


class Event(Base, DBModel, Timestampable):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    event_date = Column(DateTime)
    expenses = relationship('Expense', backref='event')

    user_id = Column(Integer, ForeignKey('users.id'))


class Payer(Base, DBModel, Timestampable):
    __tablename__ = 'payers'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    weight = Column(Integer, default=1)
    expenses = relationship('Expense', backref='payer')


class Expense(Base, DBModel, Timestampable):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(Unicode)

    event_id = Column(Integer, ForeignKey('events.id'))
    payer_id = Column(Integer, ForeignKey('payers.id'))
