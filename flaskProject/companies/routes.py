from flask import Flask, render_template, flash, redirect, url_for
from forms import CompanyRegistrationForm

from . import companies_bp

@companies_bp.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        company_type = form.company_type.data
        internship_programs = form.internship_programs.data
        duration = form.duration.data
        format = form.format.data
        requirements = form.requirements.data

        flash(f'Company registered successfully! Type: {company_type}', 'success')
        return redirect(url_for('register_company'))

    return render_template('register_company.html', form=form)