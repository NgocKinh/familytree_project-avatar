from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from backend.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    full_name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default="viewer")
    person_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)