"""
Flask Blueprint: Profile Routes
Manages user dashboards, settings, account management, and admin controls.
"""

from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from . import profile_bp
from .. import db
from ..auth.models import User
from ..survey.models import Form
from .models import Message

@profile_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Displays the logged-in user's dashboard."""
    return render_template('profile/dashboard.html', current_user=current_user)
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
    return render_template('profile/view_user_profile.html', user=user)

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


@profile_bp.route('/chat/<int:user_id>')
@login_required
def chat_with_user(user_id):
    """
    Displays chat between current user and another user.
    """
    other_user = User.query.get_or_404(user_id)

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user.id)) |
        ((Message.sender_id == other_user.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('profile/chat.html', user=other_user, messages=messages)



@profile_bp.route('/search_user')
@login_required
def search_user():
    username = request.args.get('username')
    if not username:
        flash('Please enter a username.', 'warning')
        return redirect(url_for('profile.view_chats'))

    user = User.query.filter_by(username=username).first()
    if user and user.id != current_user.id:
        return redirect(url_for('profile.chat_with_user', user_id=user.id))

    flash('User not found.', 'danger')
    return redirect(url_for('profile.view_chats'))


@profile_bp.route('/chats')
@login_required
def view_chats():
    """
    Displays recent conversations and search bar.
    """
    # Find unique users the current user has messaged or been messaged by
    messages = Message.query.filter(
        (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
    ).all()

    user_ids = set()
    for msg in messages:
        if msg.sender_id != current_user.id:
            user_ids.add(msg.sender_id)
        if msg.receiver_id != current_user.id:
            user_ids.add(msg.receiver_id)

    users = User.query.filter(User.id.in_(user_ids)).all()

    # Optional search
    search_results = None
    username_query = request.args.get('username')
    if username_query:
        search_results = User.query.filter(
            User.username.ilike(f'%{username_query}%'),
            User.id != current_user.id
        ).all()

    return render_template(
        'profile/view_chats.html',
        users=users,
        search_results=search_results
    )

@profile_bp.route('/send_message/<int:user_id>', methods=['POST'])
@login_required
def send_message(user_id):
    """
    Handles sending a message to another user.
    """
    recipient = User.query.get_or_404(user_id)
    content = request.form.get('message')

    if not content:
        flash("Message cannot be empty.", "danger")
        return redirect(url_for('profile.chat_with_user', user_id=user_id))

    new_message = Message(sender_id=current_user.id, receiver_id=recipient.id, content=content)
    db.session.add(new_message)
    db.session.commit()

    return redirect(url_for('profile.chat_with_user', user_id=user_id))

@profile_bp.route('/delete_chat/<int:user_id>', methods=['POST'])
@login_required
def delete_chat(user_id):
    try:
        other_user = User.query.get_or_404(user_id)

        Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == other_user.id)) |
            ((Message.sender_id == other_user.id) & (Message.receiver_id == current_user.id))
        ).delete(synchronize_session=False)

        db.session.commit()
        flash('Chat history deleted successfully.', 'success')

    except Exception as e:
        print(f"Delete Chat Error: {e}")
        flash('An error occurred while deleting chat history.', 'danger')

    return redirect(url_for('profile.view_chats'))
