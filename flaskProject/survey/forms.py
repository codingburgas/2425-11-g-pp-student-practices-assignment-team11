from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired
from wtforms.widgets import ListWidget, CheckboxInput



class InternshipSurveyForm(FlaskForm):
    industry = RadioField("In which industry or field do you want to grow?", choices=[
        ('it', 'a) IT & Technology'),
        ('marketing', 'b) Marketing & Advertising'),
        ('finance', 'c) Finance & Accounting'),
        ('education', 'd) Education')
    ], validators=[InputRequired()])

    company_type = RadioField("What type of company do you prefer?", choices=[
        ('startup', 'a) Small company or startup'),
        ('medium', 'b) Medium-sized company'),
        ('corporate', 'c) Large corporation'),
        ('any', 'd) No preference')
    ], validators=[InputRequired()])

    duration = RadioField("How much time are you willing to commit to the internship?", choices=[
        ('<1', 'a) Less than 1 month'),
        ('1-3', 'b) 1–3 months'),
        ('3-6', 'c) 3–6 months'),
        ('>6', 'd) More than 6 months')
    ], validators=[InputRequired()])

    skills = RadioField("What technical skills do you have?", choices=[
        ('programming', 'a) Programming (e.g. Python, Java, C++)'),
        ('data', 'b) Data Analysis'),
        ('design', 'c) Design & Visualization'),
        ('management', 'd) Project Management')
    ], validators=[InputRequired()])

    experience = RadioField("Do you have previous internship or work experience?", choices=[
        ('yes', 'a) Yes'),
        ('no', 'b) No')
    ], validators=[InputRequired()])

    format = RadioField("Do you prefer the internship to be:", choices=[
        ('on-site', 'a) On-site'),
        ('remote', 'b) Remote'),
        ('hybrid', 'c) Hybrid')
    ], validators=[InputRequired()])

    priority = RadioField("What is most important to you in the internship?", choices=[
        ('learning', 'a) Learning & Development'),
        ('environment', 'b) Good Work Environment'),
        ('salary', 'c) High Salary'),
        ('flexibility', 'd) Flexible Schedule')
    ], validators=[InputRequired()])

    teamwork = RadioField("What is your preference for teamwork?", choices=[
        ('solo', 'a) I prefer to work independently'),
        ('team', 'b) I prefer to work in a team'),
        ('neutral', 'c) No preference')
    ], validators=[InputRequired()])

    education = RadioField("What is your current level of education?", choices=[
        ('highschool', 'a) High School Student'),
        ('university', 'b) University Student'),
        ('graduate', 'c) University Graduate')
    ], validators=[InputRequired()])

    submit = SubmitField("Submit")