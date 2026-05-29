from passlib.context import CryptContext

from backend.db import SessionLocal
from backend.models.user_model import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


db = SessionLocal()

username = "admin"
password = "admin123"

existing = db.query(User).filter(User.username == username).first()

if existing:
    print("Admin user already exists")
else:
    admin_user = User(
        username=username,
        password_hash=pwd_context.hash(password),
        full_name="System Admin",
        role="admin",
        is_active=True,
    )

    db.add(admin_user)
    db.commit()

    print("Admin user created successfully")

db.close()