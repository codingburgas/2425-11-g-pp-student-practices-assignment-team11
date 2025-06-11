from flaskProject import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    company_type = db.Column(db.String(50), nullable=False)
    internship_programs = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    format = db.Column(db.String(20), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'

    def __repr__(self):
        return f'<Company {self.company_type}>'