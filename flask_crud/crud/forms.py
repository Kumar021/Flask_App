from flask_wtf import FlaskForm 
import email_validator
from wtforms import validators, StringField, SubmitField, TextField 
from wtforms.validators import DataRequired, Email 


style={'class': 'form-control form-control-sm', "style":'margin-top: -20px;'}
btn = {'class': 'btn btn-primary'}
class ContactForm(FlaskForm):
	name = StringField("Name: ", validators=[DataRequired()], render_kw=style)
	email = StringField("Email: ", validators=[DataRequired()], render_kw=style)
	message = TextField("Message :", validators=[DataRequired()], render_kw=style)
	submit = SubmitField("Submit", render_kw=btn)
