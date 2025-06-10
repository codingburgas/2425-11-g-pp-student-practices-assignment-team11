import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    SENDGRID_SENDER = os.environ.get('SENDGRID_SENDER')
