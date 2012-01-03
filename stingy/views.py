from flask import render_template

from stingy import app
from stingy.models import Event


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def event_index():
    e = Event.query.get(1)
    return render_template('event_index.html', **locals())
