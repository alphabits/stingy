from os.path import abspath, dirname


ROOT = abspath(dirname(__file__))


DB_CONNECTION_STRING = 'sqlite:///%s/data/test.db' % ROOT
