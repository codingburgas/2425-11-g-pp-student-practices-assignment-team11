from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length


class CompanyRegistrationForm(FlaskForm):
    company_type = SelectField(
        'Company Type',
        choices=[('large', 'Large Corporation'), ('medium', 'Medium Company'), ('small', 'Small Company')],
        validators=[DataRequired()]
    )
    internship_programs = SelectMultipleField(
        'Internship Programs (at least 3)',
        choices=[
            ('program1', 'Program 1'),
            ('program2', 'Program 2'),
            ('program3', 'Program 3'),
            ('program4', 'Program 4'),
            ('program5', 'Program 5')
        ],
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
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    submit = SubmitField('Register Company')