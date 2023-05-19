from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, HiddenField, PasswordField, DateTimeField, SelectField, FileField
from wtforms.validators import DataRequired, Length
from wtforms.fields import RadioField


class NewUserForm(FlaskForm):
    new_username = StringField('Username', validators=[DataRequired(), Length(min=4, max=255)])
    new_password = StringField('Password', validators=[DataRequired(), Length(min=8, max=24)])
    new_email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Create')
    
class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")