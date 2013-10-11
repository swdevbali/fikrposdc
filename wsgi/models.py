from flask_sqlalchemy import SQLAlchemy
from main import db
from collections import OrderedDict


class Users(db.Model,object):
    '''
    Adding object to trun sqlalchemy into json object
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))
    active = db.Column(db.Boolean)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    def __init__(self, username=None, password=None, email=None, firstname=None, lastname=None):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.active = True
        self.role = 'Admin'

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def _asdict(self):
        '''
        Thanks to http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        '''
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

class Companies(db.Model):
    '''
    Parent data to let this solution be applied to many company
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String)
    users = db.relation('Users', backref=db.backref('users'))
    token = db.Column(db.String) #for identification of client
    branches = db.relationship("Branches", lazy="dynamic")


    def __init__(self, name=None, address=None, token=None):
        self.name = name
        self.address = address
        self.token = token

class Branches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    address = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String) #for identification of client
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id')) #User must register first
    dailyCashFlow = db.relation('DailyCashFlow', 
                        backref=db.backref('daily_cash_flow', lazy='dynamic'),
                        cascade="all, delete-orphan",
                        lazy='dynamic',
                        passive_deletes=True)

    def __init__(self, name=None, address=None, token=None, user_id=None):
        self.name = name
        self.address = address
        self.token = token
        self.user_id = user_id

class DailyCashFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    cash_start_of_day = db.Column(db.Integer)
    cash_end_of_day = db.Column(db.Integer)
    income = db.Column(db.Integer) # which is end - start
    
    def __init__(self, day=None, cash_start_of_day = None, cash_end_of_day = None):
        self.day = day
        self.cash_start_of_day = cash_start_of_day
        self.cash_end_of_day = cash_end_of_day
        self.calculateIncome()
    
    def calculateIncome(self):
        self.income = self.cash_end_of_day - self.cash_start_of_day

    @classmethod
    def addOrUpdate(cls, **kwargs):
        branch = kwargs.pop("branch", None)
        day = kwargs.pop("day", None)
        cash_start_of_day = kwargs.pop("cash_start_of_day", None)
        cash_end_of_day = kwargs.pop("cash_end_of_day", None)

        data = DailyCashFlow.query.filter_by(branch_id = branch.id, day = day).first()
        if data is not None:
            data.cash_start_of_day = cash_start_of_day 
            data.cash_end_of_day = cash_end_of_day
            data.calculateIncome()
        else:
            data = DailyCashFlow(day=day, cash_start_of_day = cash_start_of_day, cash_end_of_day =  cash_end_of_day)
            branch.dailyCashFlow.append(data)

        db.session.commit()
        return data

db.Index('idx1', DailyCashFlow.day, DailyCashFlow.branch_id, unique = True)
