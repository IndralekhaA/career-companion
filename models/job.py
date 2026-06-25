from datetime import datetime
from extensions import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    company = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(50), nullable = False)
    date_applied = db.Column(db.Date)
    notes = db.Column(db.Text)
