import random
from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_code_email(recipient, code):
    subject = 'Your Verification Code'
    html_content = f"""
    <h2>Email Verification Code</h2>
    <p>Your verification code is:</p>
    <h3>{code}</h3>
    <br>
    <p>This email was sent from <strong>studypilot-g6gbf5gmddc7g2h3.polandcentral-01.azurewebsites.net</strong></p>
    """

    message = Mail(
        from_email=current_app.config.get('SENDGRID_SENDER', 'no-reply@studypilot.com'),
        to_emails=recipient,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(current_app.config.get('SENDGRID_API_KEY', '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'))
        response = sg.send(message)
        print(f"Email sent to {recipient}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
