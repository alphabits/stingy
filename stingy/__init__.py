from flask import Flask

import stingy.config as config
from stingy.utils import money_format


app = Flask(__name__)
app.config.from_object(config)

app.template_filter('money')(money_format)

from stingy.api import api

app.register_blueprint(api, url_prefix='/api')

import stingy.views
