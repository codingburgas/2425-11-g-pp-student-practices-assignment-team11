from flaskProject import db

class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True)
    question1 = db.Column(db.String)
    question2 = db.Column(db.String)
    question3 = db.Column(db.String)
    question4 = db.Column(db.String)
    question5 = db.Column(db.String)
    question6 = db.Column(db.String)
    question7 = db.Column(db.String)
    question8 = db.Column(db.String)
    question9 = db.Column(db.String)
    question10 = db.Column(db.String)
    question11 = db.Column(db.String)
    question12 = db.Column(db.String)
    question13 = db.Column(db.String)
    question14 = db.Column(db.String)
    question15 = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='datasets')
