from flask import render_template, redirect, url_for, flash
from .forms import InternshipSurveyForm
from . import survey_bp


@survey_bp.route('/internship_survey', methods=['GET', 'POST'])
def internship_survey():
    form = InternshipSurveyForm()
    if form.validate_on_submit():
        flash("Survey submitted successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template('survey/survey.html', form=form)