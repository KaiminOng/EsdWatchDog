from . import db

# Define models

account_endpoint = db.Table('user_endpoints', 
    db.Column('account_id', db.String(120), db.ForeignKey('account.id'), primary_key=True),
    db.Column('endpoint_url', db.String(120), db.ForeignKey('endpoint.endpoint_url'), primary_key=True)
)

endpoint_contact = db.Table('table_contacts', 
    db.Column('endpoint_url', db.String(120), db.ForeignKey('endpoint.endpoint_url'), primary_key = True),
    db.Column('chat_id', db.String(120), db.ForeignKey('contact.chat_id'), primary_key = True)
)

class Account(db.Model):

    __tablename__ = 'account'

    id = db.Column(db.String(120), primary_key = True)
    username = db.Column(db.String(80), nullable = False)
    endpoints = db.relationship('Endpoint', secondary=account_endpoint, lazy='dynamic', backref=db.backref('accounts', lazy=True))

    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __repr__(self):
        return f"User ID: {self.id} Username: {self.username}"


class Endpoint(db.Model):

    __tablename__ = 'endpoint'

    endpoint_url = db.Column(db.String(120), primary_key = True, nullable = False)
    contacts = db.relationship('Contact', secondary=endpoint_contact, lazy='dynamic', backref=db.backref('endpoints', lazy=True))

    def __init__(self, endpoint):
        self.endpoint = endpoint


class Contact(db.Model):

    __tablename__ = 'contact'

    def __init__(self, tg_chat_id):
        self.chat_id = tg_chat_id

    chat_id = db.Column(db.String(120), primary_key = True, nullable = False)
