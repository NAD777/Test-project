from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, \
    TextAreaField, MultipleFileField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired
from flask_codemirror.fields import CodeMirrorField


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
    title = StringField('Title', validators=[DataRequired()])
    mem = IntegerField('mem', validators=[DataRequired()])
    time = IntegerField('time', validators=[DataRequired()])
    difficulty = IntegerField('difficulty', validators=[DataRequired()])
    condition = TextAreaField('condition', validators=[DataRequired()])
    inp = StringField('input data', validators=[DataRequired()])
    output = StringField('output data', validators=[DataRequired()])
    files = MultipleFileField()
    col_examples = IntegerField('Col examples', validators=[DataRequired()])
    submit = SubmitField('Add')


class SendProgram(FlaskForm):
    source_code = CodeMirrorField(language='python',
                                config={'lineNumbers' : 'true'})
    
    category = SelectField(choices=[('cpp', 'C++'), ('pas', 'Pascal ABC')])
    submit = SubmitField('Отправить')