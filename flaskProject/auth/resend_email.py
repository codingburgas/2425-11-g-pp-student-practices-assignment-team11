import random
import requests
from flask import current_app

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_code_email(recipient, code):
    url = 'https://api.resend.com/emails'
    subject = 'Your Verification Code'

    html = f"""
    <h2>Email Verification Code</h2>
    <p>Your verification code is:</p>
    <h3>{code}</h3>
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
