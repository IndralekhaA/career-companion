from datetime import date, timedelta
import random

from extensions import db
from models.user import User
from models.job import Job


def seed_jobs():

    companies = [
        "Amazon",
        "Google",
        "Microsoft",
        "Meta",
        "Apple",
        "Netflix",
        "Oracle",
        "Salesforce",
        "NVIDIA",
        "Adobe",
        "Stripe",
        "Datadog",
        "Atlassian",
        "Snowflake",
        "Uber",
        "Airbnb",
        "DoorDash",
        "Coinbase",
        "LinkedIn",
        "ServiceNow"
    ]

    roles = [
        "Backend Engineer",
        "Software Engineer",
        "Python Developer",
        "Data Engineer",
        "Platform Engineer",
        "Full Stack Engineer",
        "Cloud Engineer",
        "DevOps Engineer"
    ]

    statuses = [
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ]

    users = User.query.all()

    today = date.today()

    for user in users:

        used_companies = random.sample(companies, 5)

        for i in range(5):

            job = Job(
                company=used_companies[i],
                role=random.choice(roles),
                status=random.choice(statuses),
                date_applied=today - timedelta(days=random.randint(1, 90)),
                notes="Seed Data",
                user_id=user.id
            )

            db.session.add(job)

    db.session.commit()

    print("✅ Jobs seeded successfully")