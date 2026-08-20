import os
from pathlib import Path

import mysql.connector

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
load_dotenv("backend/.env")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

required_db_config = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
}

missing_db_config = [
    name
    for name, value in required_db_config.items()
    if not value
]

if missing_db_config:
    raise RuntimeError(
        "Missing database environment variables: "
        + ", ".join(missing_db_config)
    )

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280,
)

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

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=int(DB_PORT),
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


SCHEMA_PATH = Path(__file__).resolve().parent.parent / "database" / "schema.sql"


def _read_schema_statements():
    schema_text = SCHEMA_PATH.read_text(encoding="utf-8-sig")
    executable_lines = [
        line
        for line in schema_text.splitlines()
        if not line.lstrip().startswith("--")
    ]
    return [
        statement.strip()
        for statement in "\n".join(executable_lines).split(";")
        if statement.strip()
    ]


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        for statement in _read_schema_statements():
            cursor.execute(statement)

        connection.commit()
        print("DATABASE_SCHEMA_INIT=PASS")
    finally:
        cursor.close()
        connection.close()
