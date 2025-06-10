from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://CloudSA0b7473ff:Teodor21@studypilot.database.windows.net/app'
        '?driver=ODBC+Driver+17+for+SQL+Server'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    SENDGRID_SENDER = os.environ.get("SENDGRID_SENDER")
    print("SENDGRID_API_KEY:", os.environ.get("SENDGRID_API_KEY"))
    print("SENDGRID_API_KEY:", os.environ.get("SENDGRID_SENDER"))

