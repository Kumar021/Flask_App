#from flask.ext.wtf import Form, #RecaptchaField
from wtforms import Form, SubmitField, TextField, PasswordField, BooleanField
from wtforms.validators import Required, EqualTo, Email
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
  name = TextField('NickName', [Required()])
  email = TextField('Email address', [Required(), Email()])
  password = PasswordField('Password', [Required()])
  confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
  accept_tos = BooleanField('I accept the TOS', [Required()])
  submit = SubmitField("Submit")
  #recaptcha = RecaptchaField()