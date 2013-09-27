from flask import Flask, request, flash, url_for, redirect, render_template, abort
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app) 

if __name__ == '__main__':
    app.run()
