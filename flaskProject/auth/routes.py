from flask import render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from . import auth_bp
from .forms import LoginForm, RegistrationForm, CodeForm
from .models import User
from flaskProject import login_manager, db
from .resend_email import send_verification_code_email, generate_verification_code


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main_bp.index'))
        else:
            flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        # Generate verification code
        code = generate_verification_code()
        session['verification_code'] = code
        session['verification_email'] = form.email.data
        send_verification_code_email(form.email.data, code)

        flash('Verification code sent to your email.', 'success')
        return redirect(url_for('auth.verify_code'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/verify_code', methods=['GET', 'POST'])
def verify_code():
    form = CodeForm()
    email = session.get('verification_email')
    code_sent = session.get('verification_code')

    if not email or not code_sent:
        flash("No verification in progress. Please register again.", "danger")
        return redirect(url_for('auth.register'))

    if form.validate_on_submit():
        if form.code.data == code_sent:
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True  # Make sure this field exists in your User model
                db.session.commit()
                flash("Email verified successfully! You can now log in.", "success")
                session.pop('verification_code', None)
                session.pop('verification_email', None)
                return redirect(url_for('auth.login'))
        else:
            flash("Invalid verification code.", "danger")

    return render_template('auth/verify_code.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
