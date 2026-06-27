from datetime import datetime
from extensions import db
from models.interview import Interview

class Job(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    company = db.Column(db.String(100), nullable = False)
    role = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(50), nullable = False)
    date_applied = db.Column(db.Date)
    notes = db.Column(db.Text)

    interviews = db.relationship("Interview", backref= "job", lazy = "dynamic", cascade= "all, delete-orphan")

    def get_sorted_interviews(self):
        return self.interviews.order_by(Interview.interview_date.desc()).all()
