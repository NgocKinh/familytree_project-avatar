from sqlalchemy import text

from backend.db import engine


SQL_FILE = "backend/db/create_audit_logs.sql"


def main():
    with open(SQL_FILE, "r", encoding="utf-8") as file:
        sql = file.read()

    with engine.begin() as connection:
        connection.execute(text(sql))

    print("AUDIT TABLE CREATED")


if __name__ == "__main__":
    main()