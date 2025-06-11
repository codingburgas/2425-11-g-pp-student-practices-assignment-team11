from flask import Flask, render_template, flash, redirect, url_for, session
from flask import render_template, redirect, url_for, flash
from forms import CompanyRegistrationForm
from . import companies_bp
from .models import Company


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


@companies_bp.route('/admin/companies', methods=['GET', 'POST'])
def admin_companies():
    if not session.get('role') == 'admin':  # Проверка дали потребителят е администратор
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    companies = Company.query.filter_by(status='pending').all()

    return render_template('admin_companies.html', companies=companies)


@companies_bp.route('/admin/companies/<int:company_id>/<action>', methods=['POST'])
def admin_company_action(company_id, action):
    if not session.get('role') == 'admin':
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

    return redirect(url_for('admin_companies'))