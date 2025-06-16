from flask import render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from . import auth_bp
from .forms import LoginForm, RegistrationForm, CodeForm
from .models import User
from flaskProject import login_manager, db
from .resend_email import send_verification_code_email, generate_verification_code
from ..survey.models import Form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        user_id = User.query.get(user.id).id
        survey = Form.query.filter_by(id=user_id).first()

        if user is None:
            flash('User not found. Please check your username or register.', 'danger')
            return render_template('auth/login.html', form=form)

        if not user.email_verified:
            flash('Please verify your email before logging in.', 'warning')
            return render_template('auth/login.html', form=form)

        if user.verify_password(form.password.data):
            login_user(user)
            if survey:
                return redirect(url_for('survey.survey'))
            else:
                return redirect(url_for('main_bp.index'))

        else:
            flash('Invalid password. Please try again.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data
        username = form.username.data

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register.html', form=form)

        if '@' not in email:
            flash('Email should contain "@"', 'danger')
            return render_template('auth/register.html', form=form)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('This email is already registered. Please log in or use a different email.', 'danger')
            return render_template('auth/register.html', form=form)

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('Username already taken. Please choose a different one.', 'warning')
            return render_template('auth/register.html', form=form)

        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        code = generate_verification_code()
        session['verification_code'] = code
        session['verification_email'] = email
        send_verification_code_email(email, code)

        flash('Verification code sent to your email.', 'success')
        return redirect(url_for('auth.verify_code'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        input_code = request.form.get('code')
        actual_code = session.get('verification_code')
        email = session.get('verification_email')

        if not actual_code or not email:
            flash("Verification session expired. Please register again.", "danger")
            return redirect(url_for('auth.register'))

        if input_code == actual_code:
            user = User.query.filter_by(email=email).first()
            if user:
                user.email_verified = True
                db.session.commit()
                session.pop('verification_code', None)
                session.pop('verification_email', None)

                flash("Email verified successfully! Please log in.", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("User not found.", "danger")
                return redirect(url_for('auth.register'))

        else:
            flash("Invalid verification code. Please try again.", "danger")

    return render_template('auth/verify_code.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
