from getpass import getpass

from passlib.context import CryptContext

from backend.db import SessionLocal
from backend.models.user_model import User


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def main():
    db = SessionLocal()

    try:
        if db.query(User).count() > 0:
            raise RuntimeError(
                "First Admin can only be created when the users table is empty."
            )

        username = input("Admin username: ").strip()
        full_name = input("Admin full name: ").strip()
        password = getpass("Admin password: ")
        confirmation = getpass("Confirm password: ")

        if not username:
            raise ValueError("Username is required.")

        if len(password) < 12:
            raise ValueError(
                "Password must contain at least 12 characters."
            )

        if len(password.encode("utf-8")) > 72:
            raise ValueError(
                "Password must not exceed 72 UTF-8 bytes."
            )

        if password != confirmation:
            raise ValueError("Password confirmation does not match.")

        admin = User(
            username=username,
            password_hash=pwd_context.hash(password),
            full_name=full_name or None,
            role="admin",
            person_id=None,
            is_active=True,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print(
            f"First Admin created successfully: "
            f"id={admin.id}, username={admin.username}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()