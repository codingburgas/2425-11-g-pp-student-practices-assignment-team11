from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Form
from flaskProject import db
from .forms import InternshipSurveyForm

from flaskProject.survey import survey_bp


@survey_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = InternshipSurveyForm()
    try:
        if form.validate_on_submit():
            new_form = Form(
                question1=form.industry.data,
                question2=form.company_type.data,
                question3=form.duration.data,
                question4=", ".join(form.skills.data),
                question5=form.experience.data,
                question6=form.format.data,
                question7=form.priority.data,
                question8=form.teamwork.data,
                question9=form.education.data,
                user_id=current_user.id
            )

            db.session.add(new_form)
            db.session.commit()
            if request.method == 'POST':
                flash("Survey submitted successfully!", "success")
                return redirect(url_for('main_bp.index'))
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.not_found_error'))
    return render_template("survey/survey.html", form=form)
