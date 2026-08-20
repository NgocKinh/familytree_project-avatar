from backend.password_utils import hash_password

from backend.db import SessionLocal
from backend.models.user_model import User




db = SessionLocal()

username = "admin"
password = "admin123"

existing = db.query(User).filter(User.username == username).first()

if existing:
    existing.password_hash = hash_password(password)
    existing.full_name = "System Admin"
    existing.role = "admin"
    existing.is_active = True
    existing.person_id = 1

    db.commit()
    print("Admin user reset successfully")
else:
    admin_user = User(
        username=username,
        password_hash=hash_password(password),
        full_name="System Admin",
        role="admin",
        is_active=True,
        person_id=1,
    )

    db.add(admin_user)
    db.commit()

    print("Admin user created successfully")

db.close()