from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask import render_template, redirect, url_for, flash
from flask_login import current_user

from .forms import CompanyRegistrationForm
from . import companies_bp
from .models import Company
from .. import db

companies = [
    {"name": "Microsoft", "industry": "it", "type": "corporate", "duration": "1-3", "skills": ["programming", "data"],
     "format": "hybrid"},
    {"name": "Cisco", "industry": "it", "type": "corporate", "duration": "1-3", "skills": ["programming", "management"],
     "format": "remote"},
    {"name": "Xoriant", "industry": "it", "type": "medium", "duration": "3-6", "skills": ["programming", "management"],
     "format": "on-site"},


    {"name": "P&G", "industry": "marketing", "type": "corporate", "duration": "1-3", "skills": ["data", "design"],
     "format": "hybrid"},
    {"name": "Girls in Marketing", "industry": "marketing", "type": "startup", "duration": "<1",
     "skills": ["design", "management"], "format": "remote"},
    {"name": "Samsung", "industry": "marketing", "type": "corporate", "duration": ">6",
     "skills": ["data", "management"], "format": "on-site"},

    {"name": "Cargill", "industry": "finance", "type": "corporate", "duration": "3-6", "skills": ["data", "management"],
     "format": "hybrid"},
    {"name": "Experian", "industry": "finance", "type": "corporate", "duration": "1-3",
     "skills": ["data", "programming"], "format": "remote"},
    {"name": "Melexis", "industry": "finance", "type": "medium", "duration": "3-6", "skills": ["data", "management"],
     "format": "on-site"},

    {"name": "Greenwich Public Schools", "industry": "education", "type": "corporate", "duration": "<1",
     "skills": ["management", "design"], "format": "on-site"},
    {"name": "Teach For Bulgaria", "industry": "education", "type": "corporate", "duration": "1-3",
     "skills": ["management", "data"], "format": "hybrid"},
    {"name": "EdTech Bulgaria", "industry": "education", "type": "startup", "duration": "1-3",
     "skills": ["programming", "design"], "format": "remote"},
]

@companies_bp.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = CompanyRegistrationForm()
    try:
        if form.validate_on_submit():
            new_form = Company(
                company_name = form.company_name.data,
                company_type = form.company_type.data,
                internship_one = form.internship_one.data,
                internship_two = form.internship_two.data,
                internship_three = form.internship_three.data,
                duration = form.duration.data,
                format = form.format.data,
                requirements = form.requirements.data
            )

            db.session.add(new_form)
            db.session.commit()
            if request.method == 'POST':
                flash(f'Company registered successfully!', 'success')
                return redirect(url_for('main_bp.index'))
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.unauthorized_error'))
    return render_template('companies/register_company.html', form=form)


@companies_bp.route('/admin/companies', methods=['GET', 'POST'])
def admin_companies():
    try:
        if not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('index'))

        companies = Company.query.filter_by(status='pending').all()
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.unauthorized_error'))
    return render_template('companies/admin_companies.html', companies=companies)


@companies_bp.route('/admin/companies/<int:company_id>/<action>', methods=['POST'])
def admin_company_action(company_id, action):
    try:
        if not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('index'))

        company = Company.query.get_or_404(company_id)
        if action == 'approve':
            company.status = 'approved'
            flash(f'Company {company.id} approved.', 'success')
        elif action == 'reject':
            company.status = 'rejected'
            flash(f'Company {company.id} rejected.', 'warning')
        db.session.commit()
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.unauthorized_error'))
    return redirect(url_for('companies.admin_companies'))

@companies_bp.route('/show_companies')
def show_companies():
    return render_template('companies/show_companies.html', companies=companies)


@companies_bp.route('/show_companies/apply/<company_name>', methods=['GET', 'POST'])
def apply_to_company(company_name):
    return render_template('companies/apply.html', applied_company=company_name)
