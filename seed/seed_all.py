from app import app
from extensions import db

from seed.seed_users import seed_users
from seed.seed_jobs import seed_jobs
from seed.seed_interviews import seed_interviews


with app.app_context():
    db.drop_all()
    db.create_all()

    seed_users()
    seed_jobs()
    seed_interviews()
    print("Database seeded successfully")