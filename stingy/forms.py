from wtforms import Form, TextField, IntegerField, DecimalField, SelectField,\
        validators as v

from stingy.models import Admin, Expense


class CreateEventForm(Form):
    name = TextField('Event Name', [v.Required()])
    admin_email = TextField('Your Email', [v.Required(), v.Email()])

    def create_admin(self):
        return Admin(email=self.admin_email.data)


class CreatePayerForm(Form):
    name = TextField('Name', [v.Required()])
    weight = IntegerField('How many', [v.Required()])


class CreateExpenseForm(Form):
    description = TextField('Description', [v.Required()])
    amount = DecimalField('Amount', [v.Required(), v.NumberRange(min=0)])

    payer_id = SelectField('Payer', [v.Required()], choices=[])

    def __init__(self, formdata=None, obj=None, prefix='', event=None, **kwargs):
        if not event:
            raise NameError('Event must be set')
        super(CreateExpenseForm, self).__init__(formdata, obj, prefix, **kwargs)
        self.payer_id.choices = event.get_payer_options()
        self.event = event

    def create_expense(self):
        return Expense(description=self.description.data, amount=self.amount.data,
                       event=self.event, payer_id=self.payer_id.data)
