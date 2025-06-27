"""
Flask Blueprint: Profile Routes
Manages user dashboards, settings, account management, and admin controls.
"""

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from . import profile_bp
from .. import db
from ..auth.models import User
from ..profile.models import Post

@profile_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Title and content are required', 'danger')
            return redirect(url_for('profile.dashboard'))

        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('profile.dashboard'))

    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('profile/dashboard.html', current_user=current_user, posts=posts)
@profile_bp.route('/admin')
@login_required
def admin_dashboard():
    """Admin-only dashboard displaying all users."""
    try:
        if not current_user.is_admin:
            flash('Access denied: Admins only.', 'danger')
            return redirect(url_for('auth.login'))
        users = User.query.all()
    except Exception as e:
        print(f"Admin Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return render_template('profile/admin_dashboard.html', users=users)

@profile_bp.route('/settings', methods=['GET'])
@login_required
def settings():
    """Shows user settings page."""
    return render_template('profile/settings.html', current_user=current_user)

@profile_bp.route('/update_username', methods=['POST'])
@login_required
def update_username():
    """
    Updates the user's username:
    - Ensures the username isn't empty or taken.
    """
    try:
        new_username = request.form.get('username')
        if not new_username:
            flash('Username cannot be empty', 'danger')
            return redirect(url_for('profile.settings'))

        existing = User.query.filter_by(username=new_username).first()
        if existing and existing.id != current_user.id:
            flash('Username already taken', 'danger')
            return redirect(url_for('profile.settings'))

        current_user.username = new_username
        db.session.commit()
        flash('Username updated successfully', 'success')
    except Exception as e:
        print(f"Username Update Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('profile.settings'))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """
    Changes the user's password:
    - Validates current password.
    - Ensures new password is provided.
    """
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
        print(f"Password Change Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('profile.settings'))

@profile_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """
    Deletes the current user's own account and logs them out.
    """
    try:
        user = User.query.get(current_user.id)
        logout_user()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('Your account has been deleted.', 'success')
        else:
            flash('User not found.', 'error')
    except Exception as e:
        print(f"Account Deletion Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('auth.login'))

@profile_bp.route('/user/<int:user_id>')
@login_required
def view_user_profile(user_id):
    """
    Displays a public profile page for a given user ID.
    """
    user = User.query.get_or_404(user_id)
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.id.desc()).all()
    return render_template('profile/view_user_profile.html', user=user, posts=user_posts)

@profile_bp.route('/admin/user/<int:user_id>/survey')
@login_required
def view_user_survey(user_id):
    """
    Admin-only route to view a user's survey submissions.
    """
    if not current_user.is_admin:
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('profile.admin_dashboard'))

    user = User.query.get_or_404(user_id)
    surveys = user.datasets
    return render_template('profile/admin_user_survey.html', user=user, surveys=surveys)

@profile_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """
    Admin-only route to delete another user by ID (excluding self).
    """
    try:
        if not current_user.is_admin:
            flash('Access denied: Admins only.', 'danger')
            return redirect(url_for('profile.admin_dashboard'))

        if user_id == current_user.id:
            flash("You can't delete yourself.", 'danger')
            return redirect(url_for('profile.admin_dashboard'))

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')
    except Exception as e:
        print(f"User Deletion Error: {e}")
        return redirect(url_for('errors.forbidden_error'))

    return redirect(url_for('profile.admin_view_users'))

@profile_bp.route('/users')
@login_required
def user_view_users():
    """Displays a list of all users (for any logged-in user)."""
    users = User.query.all()
    return render_template('profile/view_users.html', users=users)

@profile_bp.route('/admin/users')
@login_required
def admin_view_users():
    """Admin-only listing of all users."""
    if not current_user.is_admin:
        flash("Admins only", "danger")
        return redirect(url_for('profile.dashboard'))

    users = User.query.all()
    return render_template('profile/view_users.html', users=users, admin=True)
