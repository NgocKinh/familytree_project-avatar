from passlib.context import CryptContext

from backend.db import SessionLocal
from backend.models.user_model import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


db = SessionLocal()

username = "admin"
password = "admin123"

existing = db.query(User).filter(User.username == username).first()

if existing:
    existing.password_hash = pwd_context.hash(password)
    existing.full_name = "System Admin"
    existing.role = "admin"
    existing.is_active = True
    existing.person_id = 1

    db.commit()
    print("Admin user reset successfully")
else:
    admin_user = User(
        username=username,
        password_hash=pwd_context.hash(password),
        full_name="System Admin",
        role="admin",
        is_active=True,
        person_id=1,
    )

    db.add(admin_user)
    db.commit()

    print("Admin user created successfully")

db.close()