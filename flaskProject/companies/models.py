from flaskProject import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(80), unique=True, nullable=False)
    company_type = db.Column(db.String(50), nullable=False)
    internship_one = db.Column(db.String(200), nullable=False)
    internship_two = db.Column(db.String(200), nullable=False)
    internship_three = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(20), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')

    def __repr__(self):
        return f'<Company {self.company_type}>'