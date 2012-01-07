from flask import render_template, request, redirect, url_for, abort

from stingy import app
from stingy.forms import CreateEventForm, CreatePayerForm, CreateExpenseForm
from stingy.models import Event, Admin, Payer


def get_event_or_abort(slug):
    event = Event.get_by_slug(slug)
    if not event or event.is_deleted():
        abort(404)
    return event


@app.route('/', methods=('GET', 'POST'))
def index():
    event_form = CreateEventForm(request.form)
    events = Event.query.all()
    if request.method == 'POST' and event_form.validate():
        admin = Admin.get_by_email(event_form.admin_email.data)
        if not admin:
            admin = event_form.create_admin()
        event = Event(name=event_form.name.data, admin=admin)
        event.save()
        return redirect(url_for('event_details', slug=event.slug))
    return render_template('index.html', **locals())

@app.route('/events/<slug>', methods=('GET','POST'))
def event_details(slug):
    event = get_event_or_abort(slug)
    return render_template('event_details.html', **locals())

@app.route('/events/<slug>/payers', methods=('GET','POST'))
def payer_overview(slug):
    event = get_event_or_abort(slug)
    form = CreatePayerForm(request.form)
    if request.method == 'POST' and form.validate():
        payer = Payer(name=form.name.data, weight=form.weight.data, event=event)
        payer.save()
        return redirect(url_for('payer_overview', slug=event.slug))
    return render_template('payer_overview.html', **locals())

@app.route('/events/<slug>/expenses', methods=('GET', 'POST'))
def expense_overview(slug):
    event = get_event_or_abort(slug)
    form = CreateExpenseForm(request.form, event=event)
    if request.method == 'POST' and form.validate():
        expense = form.create_expense()
        expense.save()
        return redirect(url_for('expense_overview', slug=event.slug))
    return render_template('expense_overview.html', **locals())

@app.route('/events/<slug>/transactions')
def transaction_overview(slug):
    event = get_event_or_abort(slug)
    event.regenerate_transactions()
    return render_template('transaction_overview.html', **locals())
