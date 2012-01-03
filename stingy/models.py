from sqlalchemy import Column, Integer, String, Unicode

from stingy.database import Base, Timestampable


class Event(Base, Timestampable):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)


class User(Base, Timestampable):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)


class Expense(Base, Timestampable):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(Unicode)
