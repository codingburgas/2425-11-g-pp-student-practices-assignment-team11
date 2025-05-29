import requests
from flask import current_app


def send_verification_email(recipient, token):
    url = 'https://api.resend.com/emails'
    subject = 'Verify your email'
    link = f"http://127.0.0.1:5000/auth/verify_email/{token}"

    html = f"""
    <h2>Email Verification</h2>
    <p>Please click the link below to verify your email:</p>
    <a href="{link}">{link}</a>
    """

    payload = {
        "from": current_app.config['RESEND_SENDER'],
        "to": recipient,
        "subject": subject,
        "html": html
    }

    headers = {
        "Authorization": f"Bearer {current_app.config['RESEND_API_KEY']}",
        "Content-Type": "application/json"
    }

    requests.post(url, json=payload, headers=headers)
