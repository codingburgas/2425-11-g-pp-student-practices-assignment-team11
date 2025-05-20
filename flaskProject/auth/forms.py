from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=3, max=15, message='Username must be between 3 and 15 characters.')])
        email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email address.')])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters.')])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password', message='Passwords must match.')])
        submit = SubmitField('Register')