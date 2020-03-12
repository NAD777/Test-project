from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    nickname = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    login = StringField('Name/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Enter')