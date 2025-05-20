from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_user, logout_user, current_user

from . import auth_bp
from .forms import LoginForm, RegistrationForm
from .models import User
from flaskProject import login_manager
from flaskProject import db


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
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("the user is registered")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form, current_user=current_user)

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
