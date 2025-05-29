import os

class Config:
    SECRET_KEY = os.environ.get("StudyPilot", "super secret key")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESEND_API_KEY = 're_LXc3zdAk_NC8CdS3t5fycjzk8cXs9PtTB'
    RESEND_SENDER = 'onboarding@resend.dev'