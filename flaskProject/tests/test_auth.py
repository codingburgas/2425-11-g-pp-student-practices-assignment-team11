import pytest
from unittest.mock import patch, MagicMock
from flask import url_for


# Assuming `flaskProject.auth` is your Flask flaskProject.auth, and login() is registered at '/login'
@pytest.fixture
def client(app):
    return app.test_client()


@patch("flaskProject.auth.routes.LoginForm")
@patch("flaskProject.auth.routes.User")
def test_login_user_not_found(mock_user, mock_form, client):
    mock_form_instance = MagicMock()
    mock_form.return_value = mock_form_instance
    mock_form_instance.validate_on_submit.return_value = True
    mock_form_instance.username.data = 'nonexistent_user'

    mock_user.query.filter_by.return_value.first.return_value = None

    response = client.post('auth/login', data={'username': 'nonexistent_user', 'password': 'any'}, follow_redirects=True)
    assert b'User not found' in response.data


@patch("flaskProject.auth.routes.LoginForm")
@patch("flaskProject.auth.routes.User")
def test_login_email_not_verified(mock_user, mock_form, client):
    mock_form_instance = MagicMock()
    mock_form.return_value = mock_form_instance
    mock_form_instance.validate_on_submit.return_value = True
    mock_form_instance.username.data = 'user123'

    mock_user_instance = MagicMock()
    mock_user.query.filter_by.return_value.first.return_value = mock_user_instance
    mock_user_instance.email_verified = False

    response = client.post('auth/login', data={'username': 'user123', 'password': 'any'}, follow_redirects=True)
    assert b'Please verify your email' in response.data


@patch("flaskProject.auth.routes.login_user")
@patch("flaskProject.auth.routes.LoginForm")
@patch("flaskProject.auth.routes.User")
def test_login_success(mock_user, mock_form, mock_login_user, client):
    mock_form_instance = MagicMock()
    mock_form.return_value = mock_form_instance
    mock_form_instance.validate_on_submit.return_value = True
    mock_form_instance.username.data = 'valid_user'

    mock_user_instance = MagicMock()
    mock_user.query.filter_by.return_value.first.return_value = mock_user_instance
    mock_user_instance.email_verified = True
    mock_user_instance.verify_password.return_value = True

    response = client.post('/auth/login', data={'username': 'valid_user', 'password': 'correct'}, follow_redirects=False)
    assert response.status_code == 302
    with client.application.app_context():
        with client.application.test_request_context():
            assert response.headers['Location'].endswith(url_for('survey.survey'))


@patch("flaskProject.auth.routes.LoginForm")
@patch("flaskProject.auth.routes.User")
def test_login_invalid_password(mock_user, mock_form, client):
    mock_form_instance = MagicMock()
    mock_form.return_value = mock_form_instance
    mock_form_instance.validate_on_submit.return_value = True
    mock_form_instance.username.data = 'valid_user'

    mock_user_instance = MagicMock()
    mock_user.query.filter_by.return_value.first.return_value = mock_user_instance
    mock_user_instance.email_verified = True
    mock_user_instance.verify_password.return_value = False

    response = client.post('/auth/login', data={'username': 'valid_user', 'password': 'wrong'}, follow_redirects=True)
    assert b'Invalid password' in response.data


