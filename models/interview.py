"""
Interview model for Career Companion application.

This module defines the Interview database model and its
relationship with Job.
"""

from extensions import db
from datetime import datetime

class Interview(db.Model):
    """
    Represents one interview round for a job application.

    Relationships:
        Job(Many-to-One)

    Business Rules:
        -Every interview belongs to exactly one job.
        -A job may have multiple interviews. 
        -Exactly one interview may be marked as the final round.
    """

    __tablename__ = "interview"

    id = db.Column(db.Integer, primary_key = True)

    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable = False)

    interview_date = db.Column(db.Date, nullable = False)

    interview_time = db.Column(db.Time, nullable = False)

    interview_type = db.Column(db.String(50), nullable = False)

    round_number = db.Column(db.Integer, nullable = False)

    status = db.Column(db.String(20), nullable = False)

    result = db.Column(db.String(20), nullable = False)

    #True only for the final interview round.
    is_final_round = db.Column(db.Boolean, default = False, nullable = False)

    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    updated_at =  db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

    def __repr__(self):
        return f"<Interview {self.interview_type} | Round {self.round_number} | {self.status}>"
    
    @property
    def display_result(self):
        """
        Returns a user-friendly result label.
        """

        if self.result == "No response":
            return "Awaiting Feedback"

        return self.result

    






