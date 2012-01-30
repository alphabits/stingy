from flask import render_template, request, redirect, url_for, abort, Blueprint,\
        jsonify as json_response
from flask.views import MethodView

from stingy.forms import CreateEventForm, CreatePayerForm, CreateExpenseForm
from stingy.models import Event, Admin, Payer
from stingy.utils import data_to_multidict


api = Blueprint('api', __name__)


@api.route('/')
def api_doc():
    return render_template('api_doc.html')


class EventAPI(MethodView):

    def get(self, event_slug):
        event = Event.get_by_slug(event_slug)
        if not event:
            abort(404)
        return json_response(event.get_json_data(url_for))


    def post(self):
        form = CreateEventForm(data_to_multidict(request.json))
        if form.validate():
            admin = Admin.get_by_email(form.admin_email.data)
            if not admin:
                admin = form.create_admin()
            event = Event(
                name=form.name.data,
                admin=admin
            )
            event.save()
            return json_response(event.get_json_data(url_for))
        else:
            return json_response(form.errors)

    def put(self, event_id):
        return 'Updating existing event'

    def delete(self, event_id):
        return 'Deleting event'


event_view = EventAPI.as_view('events')
api.add_url_rule('/events/', view_func=event_view, methods=['POST'])
api.add_url_rule('/events/<event_slug>', view_func=event_view, 
        methods=['GET', 'PUT', 'DELETE'])



class ExpenseAPI(MethodView):

    def get(self, event_slug, expense_id):

        event = Event.get_by_slug(event_slug)
        if not event:
            abort(404)

        if expense_id is None:
            expenses = [expense.get_json_data(url_for) for expense in event.expenses]
            data = {'expenses': expenses}
            return json_response(data)
        else:
            expense = Expense.get_by_id_and_event_id(expense_id, event.id)
            if not expense:
                abort(404)
            return json_response(expense.get_json_data())

    def post(self, event_slug):
        return 'Creating new expense'

    def put(self, event_id, expense_id):
        return 'Updating existing expense'

    def delete(self, event_id, expense_id):
        return 'Deleting expense'

expense_view = ExpenseAPI.as_view('expenses')
api.add_url_rule('/events/<event_slug>/expenses/', view_func=expense_view, 
        methods=['GET', 'POST'], defaults={'expense_id': None})
api.add_url_rule('/events/<event_slug>/expenses/<expense_id>', view_func=expense_view, 
        methods=['GET', 'PUT', 'DELETE'])


class PayerAPI(MethodView):

    def get(self, event_slug, payer_id):
        event = Event.get_by_slug(event_slug)
        if not event:
            abort(404)

        if payer_id is None:
            payers = [payer.get_json_data(url_for) for payer in event.payers]
            data = {'payers': payers}
            return json_response(data)
        else:
            payer = Payer.get_by_id_and_event_id(payer_id, event.id)
            if not payer:
                abort(404)
            return json_response(payer.get_json_data(url_for))

    def post(self, event_slug):
        return 'Creating new payer'

    def put(self, event_id, payer_id):
        return 'Updating existing payer'

    def delete(self, event_id, payer_id):
        return 'Deleting payer'

payer_view = PayerAPI.as_view('payers')
api.add_url_rule('/events/<event_slug>/payers/', view_func=payer_view, 
        methods=['GET', 'POST'], defaults={'payer_id': None})
api.add_url_rule('/events/<event_slug>/payers/<payer_id>', view_func=payer_view, 
        methods=['GET', 'PUT', 'DELETE'])
