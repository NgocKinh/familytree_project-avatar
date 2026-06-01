from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:Msand%40167@127.0.0.1:3306/familytreedb"

engine = create_engine(DATABASE_URL)

from sqlalchemy import text

with engine.connect() as conn:
    print("DATABASE_URL =", DATABASE_URL)

    result = conn.execute(text("SELECT DATABASE(), @@hostname, @@port"))
    row = result.fetchone()
    print("DB CHECK =", row)

    result = conn.execute(text("SELECT COUNT(*) FROM users"))
    user_count = result.scalar()
    print("USER COUNT =", user_count)
    

    # result = conn.execute(text("SELECT COUNT(*) FROM family_relationships"))

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
        host="127.0.0.1",   # 🔥 đổi dòng này
        port=3306,          # 🔥 thêm dòng này
        user="root",
        password="Msand@167",
        database="familytreedb"
    )