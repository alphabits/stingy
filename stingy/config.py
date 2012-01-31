from os.path import abspath, dirname


ROOT = abspath(dirname(__file__))


DB_CONNECTION_STRING = 'sqlite:///%s/data/test.db' % ROOT


EVENT_SLUG_LENGTH = 32
ADMIN_SLUG_LENGTH = 16


LIB_SCRIPTS = [
    'libs/underscore-min.js', 
    'libs/jquery-1.7.1.min.js', 
    'libs/mustache.js', 
    'libs/backbone-min.js'
]

APP_SCRIPTS = [
    'app/main.js',
    'app/templates.js',
    'app/views.js'
]
