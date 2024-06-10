from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired

class LoginForm(Form):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])