from app import app
from extensions import db
from models.user import User
from models.job import Job
from models.interview import Interview
from werkzeug.security import generate_password_hash
from datetime import datetime, date, time

with app.app_context():

    db.drop_all()
    db.create_all()

    # ---------------- USERS ----------------
    users = []

    for i in range(1, 11):
        user = User(
            username=f"User{i}",
            email=f"user{i}@test.com",
            password_hash=generate_password_hash("Password123!")
        )
        db.session.add(user)
        users.append(user)

    db.session.commit()

    # refresh users with ids
    users = User.query.all()

    # ---------------- JOBS ----------------
    jobs = []

    statuses = ["Applied", "Interview", "Offer", "Rejected"]

    for idx, user in enumerate(users):

        for j in range(1, 6):

            job = Job(
                company=f"Company_{idx}_{j}",
                role=f"Software Engineer {j}",
                status=statuses[(j + idx) % 4],
                date_applied=date(2026, 6, j),
                notes="Seed data",
                user_id=user.id
            )

            db.session.add(job)
            jobs.append(job)

    db.session.commit()

    jobs = Job.query.all()

    # ---------------- INTERVIEWS ----------------
    for idx, job in enumerate(jobs):

        if job.status in ["Interview", "Offer"]:

            i1 = Interview(
                job_id=job.id,
                interview_date=date(2026, 7, (idx % 20) + 1),
                interview_time=time(10, 30),
                interview_type="Technical",
                round_number=1,
                status="Scheduled",
                result=None,
                notes="Round 1"
            )

            db.session.add(i1)

            i2 = Interview(
                job_id=job.id,
                interview_date=date(2026, 7, (idx % 20) + 2),
                interview_time=time(14, 0),
                interview_type="HR",
                round_number=2,
                status="Completed",
                result="Passed" if idx % 3 != 0 else "Failed",
                notes="Final round"
            )

            db.session.add(i2)

    db.session.commit()

print("FULL TEST DATA CREATED")