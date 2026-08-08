# ==========================================================
# File: backup_service.py
# Chức năng:
#     - Sao lưu dữ liệu
#     - Phục hồi dữ liệu
#     - Liệt kê danh sách backup
#     - Xóa backup
#
# RC09.1
# ==========================================================

import os
import zipfile
from datetime import datetime

from sqlalchemy import text
from backend.db import SessionLocal
# ==========================================================
# BACKUP DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

BACKUP_DIR = os.path.join(
    BASE_DIR,
    "backups"
)

# ==========================================================
# INITIALIZE
# ==========================================================

def ensure_backup_dir():
    """
    Tạo thư mục backup nếu chưa tồn tại
    """

    os.makedirs(BACKUP_DIR, exist_ok=True)

# ==========================================================
# BACKUP FILE NAME
# ==========================================================

def generate_backup_filename(
    family_code="TranAnQuan"
):
    """
    Ví dụ:

    TranAnQuan_Backup_2026-08-07_150501.zip
    """

    now = datetime.now()

    return (
        f"{family_code}_Backup_"
        f"{now.strftime('%Y-%m-%d_%H%M%S')}.zip"
    )

# ==========================================================
# EXPORT DATABASE TO SQL
# ==========================================================
def sql_value(value):
    """
    Chuyển Python value thành SQL literal
    """

    import datetime

    if value is None:
        return "NULL"

    if isinstance(value, bool):
        return "1" if value else "0"

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, datetime.datetime):
        return "'" + value.strftime("%Y-%m-%d %H:%M:%S") + "'"

    if isinstance(value, datetime.date):
        return "'" + value.strftime("%Y-%m-%d") + "'"

    text_value = str(value)
    text_value = text_value.replace("\\", "\\\\")
    text_value = text_value.replace("'", "''")

    return "'" + text_value + "'"

def export_database_sql(output_path):

    db = SessionLocal()

    try:
        with open(output_path, "w", encoding="utf-8") as f:

            f.write("-- FamilyTree Database Backup\n")
            f.write("-- Generated automatically\n\n")

            f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")

            tables = db.execute(
                text("SHOW TABLES")
            ).fetchall()

            for row in tables:

                table_name = row[0]

                # --------------------------------------------------
                # CREATE TABLE
                # --------------------------------------------------

                result_create = db.execute(
                    text(f"SHOW CREATE TABLE `{table_name}`")
                )

                create_sql = result_create.fetchone()[1]

                f.write(create_sql)
                f.write(";\n\n")

                # --------------------------------------------------
                # COLUMN LIST
                # --------------------------------------------------

                result_columns = db.execute(
                    text(f"SHOW COLUMNS FROM `{table_name}`")
                )

                columns = [
                    col[0]
                    for col in result_columns
                ]

                # --------------------------------------------------
                # TABLE DATA
                # --------------------------------------------------

                rows = db.execute(
                    text(f"SELECT * FROM `{table_name}`")
                ).fetchall()

                if not rows:
                    continue

                f.write(
                    f"INSERT INTO `{table_name}`\n"
                )

                f.write("(")

                f.write(
                    ", ".join(
                        f"`{c}`"
                        for c in columns
                    )
                )

                f.write(")\nVALUES\n")

                values_sql = []

                for data_row in rows:

                    values = [
                        sql_value(value)
                        for value in data_row
                    ]

                    values_sql.append(
                        "(" + ", ".join(values) + ")"
                    )

                f.write(
                    ",\n".join(values_sql)
                )

                f.write(";\n\n")

            f.write("SET FOREIGN_KEY_CHECKS=1;\n")

    finally:
        db.close()

# ==========================================================
# CREATE EMPTY BACKUP
# ==========================================================

def create_backup_zip():

    ensure_backup_dir()

    filename = generate_backup_filename()

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    sql_path = os.path.join(
        BACKUP_DIR,
        "database.sql"
    )

    export_database_sql(sql_path)
    
    with zipfile.ZipFile(
        filepath,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        zipf.write(sql_path, "database.sql")

        zipf.writestr(
            "README.txt",
            "FamilyTree Backup\n"
        )

        zipf.writestr(
            "version.txt",
            "FamilyTree Version 1.0\n"
        )

    return filename

# ==========================================================
# LIST BACKUP FILES
# ==========================================================

def list_backup_files():

    ensure_backup_dir()

    files = []

    for filename in os.listdir(BACKUP_DIR):

        if filename.endswith(".zip"):

            files.append(filename)

    files.sort(reverse=True)

    return files