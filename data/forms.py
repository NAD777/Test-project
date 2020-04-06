from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField,  MultipleFileField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Repeat password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    login = StringField('Name/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Enter')


class AddProblem(FlaskForm):
    title = StringField('Title')
    mem = IntegerField('mem')
    time = IntegerField('time')
    difficulty = IntegerField('difficulty')
    condition = TextAreaField('condition')
    inp = StringField('input data')
    output = StringField('output data')
    files = MultipleFileField()
    submit = SubmitField('Add')
