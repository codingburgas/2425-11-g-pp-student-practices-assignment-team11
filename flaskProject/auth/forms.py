from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField("Register")

class CodeForm(FlaskForm):
    code = StringField('Enter 6-digit Code', validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')
