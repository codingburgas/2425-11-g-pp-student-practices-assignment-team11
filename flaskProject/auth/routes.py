from flask import render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from . import auth_bp
from .forms import LoginForm, RegistrationForm
from .models import User
from flaskProject import login_manager
from flaskProject import db
from .resend_email import send_verification_email


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
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form = form, current_user=current_user)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if "@" in form.email.data:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            email = form.email.data
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(email, salt='email-confirm')
            send_verification_email(email, token)
            return redirect(url_for('auth.login'))
        else:
            flash("Invalid email")
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form = form, current_user=current_user)

@auth_bp.route('/verify_email/<token>')
def verify_email(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=3600)
        confirmed = True
    except (SignatureExpired, BadSignature):
        confirmed = False
    return render_template('auth/verify_email.html', confirmed=confirmed)
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
