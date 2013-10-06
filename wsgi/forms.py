from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional

class LoginForm(Form):
    username = TextField('Username', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password'))
            ])
    password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password'))
            ])
    remember_me = BooleanField('Remember me', default = False)

class UserForm(Form):
    id = HiddenField()
    username = TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password')),
            EqualTo('password_confirm', message='Passwords must match')
            ])
    password_confirm = PasswordField('Confirm password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password')),
            ])
    email = TextField('Email', validators=[
            Required(),
            validators.Length(min=6, message=(u'Little short for an email address?')),
            validators.Email(message=(u'That\'s not a valid email address.'))
            ])

class BranchForm(Form):
    id = HiddenField()
    name = TextField('Name', validators=[
            Required(),
            validators.Length(min=2, message=(u'Please give a longer branch name'))
            ])
    address = TextAreaField('Address', validators=[
            Optional(),
            validators.Length(max=200, message=(u'Maximum of 200 character please'))
            ])
    token = TextField('Token', validators=[
            Required(),
            validators.Length(min=6, message=(u'At least 6 characters'))
            ])

class RegistrationForm(Form):
    username = TextField('Username', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password'))
            ])
    firstname = TextField('First Name', validators=[Required()])
    lastname = TextField('Last Name', validators=[Required()])
    agree = BooleanField('I agree all your <a href="/tos">Terms of Services</a>', validators=[Required()])
    password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password')),
            EqualTo('password_confirm', message='Passwords must match')
            ])
    password_confirm = PasswordField('Confirm password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password')),
            ])
    email = TextField('Email', validators=[
            Required(),
            validators.Length(min=6, message=(u'Little short for an email address?')),
            validators.Email(message=(u'That\'s not a valid email address.'))
            ])
    company_name = TextField('Company Name', validators=[
            Required(),
            validators.Length(min=2, message=(u'Please give a longer branch name'))
            ])
