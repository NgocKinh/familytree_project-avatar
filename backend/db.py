from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:Msand%40167@localhost/family_test"

engine = create_engine(DATABASE_URL)

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
        host="localhost",
        user="root",
        password="Msand@167",
        database="family_test"
    )