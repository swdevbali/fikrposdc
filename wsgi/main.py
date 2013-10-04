from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


import models, views 

if __name__ == '__main__':
    from main import app as application
    from main import *
    print ' - Create DB and run application..'
    
    db.create_all()
    app.run(debug=True)
