import os

class Config:
    SECRET_KEY = os.environ.get("StudyPilot", "super secret key")
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://CloudSA0b7473ff:Teodor21@studypilot.database.windows.net/app?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESEND_API_KEY = 're_LXc3zdAk_NC8CdS3t5fycjzk8cXs9PtTB'
    RESEND_SENDER = 'onboarding@resend.dev'
