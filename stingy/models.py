from sqlalchemy import Column, Integer, String, Unicode, DateTime, ForeignKey,\
        Numeric, Enum, Float
from sqlalchemy.orm import relationship

from stingy.config import EVENT_SLUG_LENGTH, ADMIN_SLUG_LENGTH
from stingy.database import Base, Timestampable, DBModel
from stingy.utils import get_random_string


def get_admin_slug():
    return get_random_string(length=ADMIN_SLUG_LENGTH)

class Admin(Base, DBModel, Timestampable):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode)
    slug = Column(String, default=get_admin_slug)
    events = relationship('Event', backref='admin')

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email==email).first()


def get_event_slug():
    return get_random_string(length=EVENT_SLUG_LENGTH)

class Event(Base, DBModel, Timestampable):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    slug = Column(String, default=get_event_slug)
    name = Column(Unicode)
    status = Column(Enum('active', 'closed', 'deleted'), default='active')
    expenses = relationship('Expense', backref='event', lazy='joined')
    payers = relationship('Payer', backref='event', lazy='joined')
    transactions = relationship('Transaction', backref='event')

    admin_id = Column(Integer, ForeignKey('admins.id'))

    @property
    def name_label(self):
        append = '' if self.is_active() else ' (%s)' % self.status
        return self.name + append

    @property
    def total_expenses(self):
        return sum([e.amount for e in self.expenses])

    @property
    def total_weight(self):
        return sum([p.weight for p in self.payers])

    @property
    def amount_pr_person(self):
        weight = self.total_weight
        if weight == 0:
            return 0
        return self.total_expenses/self.total_weight

    def get_json_data(self, url_for):
        links = {
            'self': url_for('api.events', event_slug=self.slug),
            '/rels/event-expenses': url_for('api.expenses', event_slug=self.slug)
        }
        return dict(
            id=self.id,
            slug=self.slug,
            name=self.name,
            status=self.status,
            links=links,
            amount_pr_person=self.amount_pr_person
        )

    def is_viewable(self):
        return self.status in ['active', 'closed']

    def is_active(self):
        return self.status == 'active'

    def is_deleted(self):
        return self.status == 'deleted'

    def get_payer_options(self):
        return [(str(p.id), p.name) for p in self.payers]

    def regenerate_transactions(self):
        self.delete_transactions()
        self.generate_transactions()

    def delete_transactions(self):
        for transaction in self.transactions:
            transaction.delete()

    def generate_transactions(self):
        if len(self.payers) < 2:
            return
        while self.unbalanced_payer_exists():
            self.balance_one_payer()

    def unbalanced_payer_exists(self):
        for p in self.payers:
            if not p.in_balance():
                return True
        return False

    def balance_one_payer(self):
        payers = list(self.payers)
        payers.sort(key=lambda p: p.balance_with_transactions)

        largest_debitor = payers[0]
        largest_creditor = payers[-1]
        if abs(largest_debitor.balance_with_transactions) > largest_creditor.balance_with_transactions:
            payer_to_balance = largest_debitor
        else:
            payer_to_balance = largest_creditor
        self._balance_one_payer(payer_to_balance, payers)

    def _balance_one_payer(self, payer, all_payers):
        if payer.is_creditor():
            all_payers.reverse()
        while not payer.in_balance() and all_payers:
            if payer.is_creditor():
                from_ = all_payers.pop()
                to = payer
            else:
                from_ = payer
                to = all_payers.pop()
            amount = min(abs(from_.get_balance()), abs(to.get_balance()))
            t = Transaction(from_=from_, to=to, event=self, amount=amount)
            t.save()

    @classmethod
    def get_by_slug(cls, slug):
        return cls.query.filter(cls.slug==slug).first()


class Payer(Base, DBModel, Timestampable):
    __tablename__ = 'payers'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    weight = Column(Integer, default=1)
    expenses = relationship('Expense', backref='payer', lazy='joined')
    transactions_in = relationship('Transaction', backref='to', primaryjoin='Payer.id==Transaction.to_id')
    transactions_out = relationship('Transaction', backref='from_', primaryjoin='Payer.id==Transaction.from_id')

    event_id = Column(Integer, ForeignKey('events.id'))

    @property
    def total_expenses(self):
        total = 0
        for expense in self.expenses:
            total += expense.amount
        return total

    @property
    def balance(self):
        return self.total_expenses - self.weight*self.event.amount_pr_person

    @property
    def transaction_balance(self):
        return self.total_transactions_out - self.total_transactions_in

    @property
    def balance_with_transactions(self):
        return self.balance + self.transaction_balance
    
    @property
    def total_transactions_out(self):
        return sum([t.amount for t in self.transactions_out])

    @property
    def total_transactions_in(self):
        return sum([t.amount for t in self.transactions_in])

    def get_balance(self, including_transactions=True):
        return self.balance_with_transactions if including_transactions else self.balance

    def in_balance(self, including_transactions=True):
        return abs(self.get_balance(including_transactions)) < 0.1

    def is_creditor(self, including_transactions=True):
        return self.get_balance(including_transactions) > 0

    def get_json_data(self, url_for):
        return dict(
            id=self.id, 
            name=self.name, 
            weight=self.weight,
            links={
                'self': url_for('api.payers', event_slug=self.event.slug, payer_id=self.id)
            }
        )

    @classmethod
    def get_by_id_and_event_id(cls, id, event_id):
        return cls.query.filter((cls.id==id) & (cls.event_id==event_id)).first()


class Expense(Base, DBModel, Timestampable):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(Unicode)
    amount = Column(Float)

    event_id = Column(Integer, ForeignKey('events.id'))
    payer_id = Column(Integer, ForeignKey('payers.id'))

    def get_json_data(self, url_for):
        return dict(
            id=self.id, 
            description=self.description, 
            amount=self.amount,
            links={
                'self': url_for('api.expenses', event_slug=self.event.slug),
                '/rels/expense-payer': url_for('api.payers', event_slug=self.event.slug, payer_id=self.payer_id)
            }
        )

    @classmethod
    def get_by_id_and_event_id(cls, id, event_id):
        return cls.query.filter((cls.id==id) & (cls.event_id==event_id)).first()


class Transaction(Base, DBModel, Timestampable):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    status = Column(Enum('pending', 'payed'), default='pending')

    from_id = Column(Integer, ForeignKey('payers.id'))
    to_id = Column(Integer, ForeignKey('payers.id'))
    event_id = Column(Integer, ForeignKey('events.id'))


