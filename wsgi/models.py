from flask_sqlalchemy import SQLAlchemy
from main import db
from collections import OrderedDict


class Company(db.Model):
    '''
    Parent data to let this solution be applied to many company
    '''
    __tablename__ = 'companies'
    id = db.Column('company_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    address = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) #User must register first
    token = db.Column(db.String) #for identification of client

class Users(db.Model,object):
    '''
    Adding object to trun sqlalchemy into json object
    '''
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.String(20))
    active = db.Column(db.Boolean)
    branches = db.relationship('Branches', backref = 'admin', lazy = 'dynamic')

    def __init__(self, username, password, email):
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

class Branches(db.Model):
    __tablename__ = 'branches'
    id = db.Column('branch_id', db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    address = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, name, address):
        """define user_id/admin of this branch later
        """
        self.name = name
        self.address = address
