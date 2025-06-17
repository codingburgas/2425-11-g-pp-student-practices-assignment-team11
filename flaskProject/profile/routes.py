from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from . import profile_bp
from .. import db
from ..auth.models import User
from ..survey.models import Form

@profile_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('profile/dashboard.html', current_user=current_user)

@profile_bp.route('/admin')
@login_required
def admin_dashboard():
    try:
        if not current_user.is_admin:
            flash('Access denied: Admins only.', 'danger')
            return redirect(url_for('auth.login'))

        users = User.query.all()
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.forbidden_error'))
    return render_template('profile/admin_dashboard.html', users=users)

@profile_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    return render_template('profile/settings.html', current_user=current_user)

@profile_bp.route('/update_username', methods=['POST'])
@login_required
def update_username():
    try:
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
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.forbidden_error'))
    return redirect(url_for('profile.settings'))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        current_pw = request.form.get('current_password')
        new_pw = request.form.get('new_password')

        if not current_pw or not new_pw:
            flash('Both fields are required', 'danger')
            return redirect(url_for('profile.settings'))

        if not current_user.verify_password(current_pw):
            flash('Current password incorrect', 'danger')
            return redirect(url_for('profile.settings'))

        current_user.password = new_pw
        db.session.commit()
        flash('Password updated successfully', 'success')
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.forbidden_error'))
    return redirect(url_for('profile.settings'))

@profile_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        user_id = current_user.id
        user = User.query.get(user_id)
        logout_user()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been deleted.', category='success')
        else:
            flash('User not found.', category='error')
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.forbidden_error'))
    return redirect(url_for('auth.login'))

# ✅ NEW: View public user profile (username only)
@profile_bp.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile/view_user_profile.html', user=user)

# ✅ NEW: Admin view of user survey results
@profile_bp.route('/admin/user/<int:user_id>/survey')
@login_required
def view_user_survey(user_id):
    if not current_user.is_admin:
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('profile.admin_dashboard'))

    user = User.query.get_or_404(user_id)
    surveys = user.datasets
    return render_template('profile/admin_user_survey.html', user=user, surveys=surveys)

# ✅ NEW: Admin delete user
@profile_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    try:
        if not current_user.is_admin:
            flash('Access denied: Admins only.', 'danger')
            return redirect(url_for('profile.admin_dashboard'))

        user = User.query.get_or_404(user_id)

        if user.id == current_user.id:
            flash("You can't delete yourself.", 'danger')
            return redirect(url_for('profile.admin_dashboard'))

        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')
    except Exception as e:
        print(f"Login Error: {e}")
        return redirect(url_for('errors.forbidden_error'))
    return redirect(url_for('profile.admin_dashboard'))
