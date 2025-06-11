from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flaskProject import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    __password = db.Column("password", db.String(300), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    datasets = db.relationship('Form', back_populates='user', cascade='all, delete')

    @property
    def password(self):
        return AttributeError('password is not a valid')

    @password.setter
    def password(self, password):
        self.__password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.__password, password)

    def __repr__(self):
        return f'<User {self.username}>'
