from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from . import profile_bp
from .. import db
from ..auth.models import User

@profile_bp.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template('profile/dashboard.html', current_user=current_user)
@profile_bp.route('/admin')
def admin_dashboard():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('auth.login'))

    users = User.query.all()
    return render_template('profile/admin_dashboard.html', users=users)
@profile_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('profile/settings.html', current_user=current_user)


@profile_bp.route('/update_username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form.get('username')
    if not new_username:
        flash('Username cannot be empty', 'danger')
        return redirect(url_for('profile.settings'))

    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user and existing_user.id != current_user.id:
        flash('Username already taken', 'danger')
        return redirect(url_for('profile.settings'))

    current_user.username = new_username
    db.session.commit()
    flash('Username updated successfully', 'success')
    return redirect(url_for('profile.settings'))


@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_pw = request.form.get('current_password')
    new_pw = request.form.get('new_password')

    if not current_pw or not new_pw:
        flash('Both fields are required', 'danger')
        return redirect(url_for('profile.settings'))

    if not current_user.verify_password(current_pw):
        flash('Current password incorrect', 'danger')
        return redirect(url_for('profile.settings'))

    current_user.password_hash = generate_password_hash(new_pw)
    db.session.commit()
    flash('Password updated successfully', 'success')
    return redirect(url_for('profile.settings'))


@profile_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id
    user = User.query.get(user_id)
    logout_user()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Your account has been deleted.', category='success')
    else:
        flash('User not found.', category='error')
    return redirect(url_for('auth.login'))


