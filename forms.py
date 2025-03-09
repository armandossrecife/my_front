from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms import validators
from wtforms.validators import EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField(render_kw={"class": "form-control"})
    password = PasswordField(render_kw={"class": "form-control"})
    submit = SubmitField('Logar', render_kw={"class": "btn btn-primary"})

class RegisterForm(FlaskForm):
    name = StringField('Full name', [validators.DataRequired()], render_kw={"class": "form-control"})
    username = EmailField('Email', [validators.DataRequired(), validators.Email()], render_kw={"class": "form-control"})
    password = PasswordField('Password', [validators.DataRequired(), Length(min=6, message='A senha deve ter pelo menos 6 caracteres.')],render_kw={"class": "form-control"})
    password2 = PasswordField('Password2', [validators.DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')], render_kw={"class": "form-control"})
    submit = SubmitField('Register', render_kw={"class": "btn btn-primary"})