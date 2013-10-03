from flask_sqlalchemy import SQLAlchemy
from main import db
from collections import OrderedDict


class Users(db.Model,object):
    '''
    Adding object to trun sqlalchemy into json object
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))
    active = db.Column(db.Boolean)


    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.email = email
        self.password = password
        self.active = True
        self.role = 'Admin'

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id')) #User must register first
    token = db.Column(db.String) #for identification of client
    branches = db.relationship("Branches")


    def __init__(self, name, address, user_id, token):
        self.name = name
        self.address = address
        self.user_id = user_id
        self.token = token

class Branches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    address = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    token = db.Column(db.String) #for identification of client
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id')) #User must register first

    def __init__(self, name=None, address=None, token=None, user_id=None):
        self.name = name
        self.address = address
        self.token = token
        self.user_id = user_id
