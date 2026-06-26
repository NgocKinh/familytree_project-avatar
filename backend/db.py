import os
import mysql.connector

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
load_dotenv("backend/.env")

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "familytreedb")

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280,
)

from sqlalchemy import text

with engine.connect() as conn:

    result = conn.execute(text("SELECT DATABASE(), @@hostname, @@port"))
    row = result.fetchone()

    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    user_count = result.scalar()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# 👇 CÁI BẠN THIẾU
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )