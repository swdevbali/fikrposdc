from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField
from wtforms.validators import Required, EqualTo

class UserForm(Form):
    id = HiddenField()
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=4, message=(u'Please give a longer password')),
            EqualTo('password_confirm', message='Passwords must match')
            ])
    password_confirm = PasswordField('Confirm password', validators=[
            Required(),
            validators.Length(min=4, message=(u'Please give a longer password')),
            ])
    email = TextField('Email', validators=[
            Required(),
            validators.Length(min=6, message=(u'Little short for an email address?')),
            validators.Email(message=(u'That\'s not a valid email address.'))
            ])
