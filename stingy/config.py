from os.path import abspath, dirname


ROOT = abspath(dirname(__file__))


DB_CONNECTION_STRING = 'sqlite:///%s/data/test.db' % ROOT


EVENT_SLUG_LENGTH = 32
ADMIN_SLUG_LENGTH = 16
