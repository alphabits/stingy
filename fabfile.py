from __future__ import with_statement
import os

from stingy.config import DB_CONNECTION_STRING
from stingy.database import init_db



def empty_db():
    path = DB_CONNECTION_STRING.replace('sqlite:///', '')
    os.remove(path)
    with open(path, 'w') as f:
        pass
