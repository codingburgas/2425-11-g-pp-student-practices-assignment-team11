import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://CloudSA0b7473ff:Teodor21@studypilot.database.windows.net/app'
        '?driver=ODBC+Driver+17+for+SQL+Server'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENDGRID_API_KEY = os.environ.get(
        'SENDGRID_API_KEY',
        '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'
    )
    SENDGRID_SENDER = os.environ.get(
        'SENDGRID_SENDER',
        'no-reply@studypilot.com'
    )
