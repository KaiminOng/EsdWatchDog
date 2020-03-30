from . import db

# Define models

# account_endpoint = db.Table('user_endpoints', 
#     db.Column('account_id', db.String(120), db.ForeignKey('account.id'), primary_key=True),
#     db.Column('endpoint_url', db.String(120), db.ForeignKey('endpoint.endpoint_url'), primary_key=True)
# )

# endpoint_contact = db.Table('table_contacts', 
#     db.Column('endpoint_url', db.String(120), db.ForeignKey('endpoint.endpoint_url'), primary_key = True),
#     db.Column('chat_id', db.String(120), db.ForeignKey('contact.chat_id'), primary_key = True)
# )

class accountEndpoint(db.Model):

    __tablename__ = 'accountEndpoint'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(120), db.ForeignKey("account.id"), nullable=False)
    endpoint_url = db.Column(db.String(120), db.ForeignKey("endpoint.endpoint_url"), nullable=False)
    # chat_id = db.Column(db.Integer, db.ForeignKey("contact.chat_id"), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey("contact.chat_id"), nullable=False)


    __table_args__ = (db.UniqueConstraint(account_id, endpoint_url, chat_id), )
    
    account = db.relationship('Account', backref="watchlist")
    endpoint = db.relationship('Endpoint', backref="watchers")
    contact = db.relationship("Contact",
                    primaryjoin="and_(accountEndpoint.account_id==Contact.chat_owner_id, "
                        "accountEndpoint.chat_id==Contact.chat_id)")


class Account(db.Model):

    __tablename__ = 'account'

    id = db.Column(db.String(120), primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique=True)
    contacts = db.relationship('Contact')


class Endpoint(db.Model):

    __tablename__ = 'endpoint'

    endpoint_url = db.Column(db.String(120), primary_key = True)
    status = db.Column(db.String(20))
    last_checked = db.Column(db.Integer)
    events = db.relationship('Monitoring', backref='endpoint')


    def update_status(self, status, last):
        """Updates the status and last checked time for endpoint object"""
        self.status = status
        self.last_checked = last


class Contact(db.Model):

    __tablename__ = 'contact'

    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    chat_owner_id = db.Column(db.String(120), db.ForeignKey("account.id"), primary_key=True)
    chat_title = db.Column(db.String(120))
    chat_type = db.Column(db.String(20))


class Monitoring(db.Model):

    __tablename__ = 'monitoring'

    event_id = db.Column(db.Integer, primary_key=True)
    # Endpoint many to one relationship
    endpoint_url = db.Column(db.String(120), db.ForeignKey('endpoint.endpoint_url'), nullable=False)
    timestamp = db.Column(db.Integer)
    status = db.Column(db.String(10), nullable = False)


    __table_args__ = (db.UniqueConstraint(endpoint_url, timestamp),)

