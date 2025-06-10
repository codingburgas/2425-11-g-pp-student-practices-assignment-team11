import os


class Config:
    SECRET_KEY = "super-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://CloudSA0b7473ff:Teodor21@studypilot.database.windows.net/app'
        '?driver=ODBC+Driver+17+for+SQL+Server'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    SENDGRID_SENDER = 'tdtanev21@codingburgas.bg'
