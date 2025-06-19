"""
Flask Blueprint: Authentication Routes
Handles login, logout, registration, email verification, and session flows.
"""

from flask import render_template, redirect, url_for, flash, session, request
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
    """Loads a user by ID for Flask-Login session management."""
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login endpoint:
    - Validates credentials and email verification.
    - Redirects new users to complete survey.
    """
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                flash('User not found. Please check your username or register.', 'danger')
                return render_template('auth/login.html', form=form)

            if not user.email_verified:
                flash('Please verify your email before logging in.', 'warning')
                return render_template('auth/login.html', form=form)

            if user.verify_password(form.password.data):
                login_user(user)
                survey = Form.query.filter_by(id=user.id).first()
                if survey:
                    return redirect(url_for('main_bp.index'))
                return redirect(url_for('survey.survey'))
            else:
                flash('Invalid password. Please try again.', 'danger')
    except Exception as e:
        print(f"Login Error: {e}")
        flash('A critical error occurred.', 'danger')
        return redirect(url_for('errors.integrity_error'))

    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration endpoint:
    - Validates form inputs.
    - Creates new user and sends a verification code.
    """
    form = RegistrationForm()
    try:
        if request.method == 'POST':
            password = form.password.data
            confirm = form.confirm_password.data
            email = form.email.data
            username = form.username.data

            if password != confirm:
                flash('Passwords do not match', 'danger')
                return render_template('auth/register.html', form=form)

            if '@' not in email:
                flash('Email should contain "@"', 'danger')
                return render_template('auth/register.html', form=form)

            if User.query.filter_by(email=email).first():
                flash('This email is already registered. Please log in or use a different email.', 'danger')
                return render_template('auth/register.html', form=form)

            if User.query.filter_by(username=username).first():
                flash('Username already taken.', 'warning')
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
    except Exception as e:
        print(f"Registration Error: {e}")
        return redirect(url_for('errors.integrity_error'))

    return render_template('auth/register.html', form=form)

@auth_bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    """
    Verifies the emailed code:
    - Matches user session code and marks email as verified.
    """
    try:
        if request.method == 'POST':
            input_code = request.form.get('code')
            actual = session.get('verification_code')
            email = session.get('verification_email')

            if not actual or not email:
                flash("Verification session expired. Please register again.", "danger")
                return redirect(url_for('auth.register'))

            if input_code == actual:
                user = User.query.filter_by(email=email).first()
                if user:
                    user.email_verified = True
                    db.session.commit()
                    session.pop('verification_code', None)
                    session.pop('verification_email', None)
                    flash("Email verified successfully! Please log in.", "success")
                    return redirect(url_for('auth.login'))
                flash("User not found.", "danger")
                return redirect(url_for('auth.register'))
            else:
                flash("Invalid verification code. Please try again.", "danger")
    except Exception as e:
        print(f"Verification Error: {e}")
        return redirect(url_for('errors.internal_error'))

    return render_template('auth/verify_code.html')

@auth_bp.route('/logout')
def logout():
    """Logs out the current user and redirects to homepage."""
    logout_user()
    return redirect(url_for('main_bp.index'))
