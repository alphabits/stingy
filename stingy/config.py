from os.path import abspath, dirname


ROOT = abspath(dirname(__file__))


DB_CONNECTION_STRING = 'sqlite:///{0}/data/test.db'.format(ROOT)
