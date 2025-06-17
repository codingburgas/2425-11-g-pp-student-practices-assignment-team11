from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length


class CompanyRegistrationForm(FlaskForm):
    company_name = TextAreaField(
        'Company Name',
        validators=[DataRequired()]
    )
    company_type = SelectField(
        'Company Type',
        choices=[('large', 'Large Corporation'), ('medium', 'Medium Company'), ('small', 'Small Company')],
        validators=[DataRequired()]
    )
    internship_one = TextAreaField(
        'Internship #1',
        validators=[DataRequired()]
    )
    internship_two = TextAreaField(
        'Internship #2',
        validators=[DataRequired()]
    )
    internship_three = TextAreaField(
        'Internship #3',
        validators=[DataRequired()]
    )
    duration = IntegerField('Duration (in months)', validators=[DataRequired()])
    format = SelectField(
        'Format',
        choices=[('remote', 'Remote'), ('in_person', 'In-Person'), ('hybrid', 'Hybrid')],
        validators=[DataRequired()]
    )
    requirements = TextAreaField(
        'Requirements',
        validators=[DataRequired()]
    )
    submit = SubmitField('Register Company')