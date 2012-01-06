from datetime import datetime

from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from stingy.config import DB_CONNECTION_STRING


engine = create_engine(DB_CONNECTION_STRING, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import stingy.models
    Base.metadata.create_all(bind=engine)


class DBModel(object):

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Timestampable(object):
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
