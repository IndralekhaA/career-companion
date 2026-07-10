from datetime import date, time, timedelta
import random

from extensions import db
from models.job import Job
from models.interview import Interview


def seed_interviews():
    jobs = Job.query.all()
    today = date.today()
    created = 0

    for job in jobs:
        if job.status == "Applied":
            continue
        interview1 = Interview(
            job_id = job.id,
            interview_date = today - timedelta(days=random.randint(3,15)),
            interview_time = time(10,0),
            interview_type = "Technical",
            round_number = 1,
            status = "Completed",
            result= "Passed",
            is_final_round= False,
            notes="Seed Data"


        )

        interview2 = Interview(
        job_id=job.id,
        interview_date=today + timedelta(days=random.randint(2,10)),
        interview_time=time(14,0),
        interview_type="Manager",
        round_number=2,
        status="Scheduled",
        result="Awaiting Response",
        is_final_round=False,
        notes="Seed Data"
        )

        db.session.add(interview1)
        db.session.add(interview2)

        created += 2
    
    db.session.commit()

    print(f"✅ {created} interviews created.")