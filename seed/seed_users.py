from werkzeug.security import generate_password_hash
from models.user import User
from extensions import db



def seed_users():

    users = [
        ("Alice Johnson", "alice@test.com"),
        ("Bob Smith", "bob@test.com"),
        ("Charlie Brown", "charlie@test.com"),
        ("David Miller", "david@test.com"),
        ("Emma Wilson", "emma@test.com"),
        ("Frank Thomas", "frank@test.com"),
        ("Grace Lee", "grace@test.com"),
        ("Henry Adams", "henry@test.com"),
        ("Isabella Clark", "isabella@test.com"),
        ("Jack Taylor", "jack@test.com"),
    ]

    created_users = []

    for username, email in users:

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash("Password123!")
        )

        db.session.add(user)
        created_users.append(user)

    db.session.commit()

    print("✅ 10 users created")

    return created_users