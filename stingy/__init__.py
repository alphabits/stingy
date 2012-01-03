from flask import Flask

import stingy.config as config


app = Flask(__name__)
app.config.from_object(config)


import stingy.views
