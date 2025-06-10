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
        'tdtanev21@codingburgas.bg'
    )
