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
from backend.database import SessionLocal
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

def export_database_sql(output_path):

    db = SessionLocal()

    try:
        with open(output_path, "w", encoding="utf-8") as f:

            f.write("-- FamilyTree Database Backup\n")
            f.write("-- Generated automatically\n\n")

            result = db.execute(
                text("SHOW TABLES")
            )

            for row in result:

                table_name = row[0]

                print(table_name)

                f.write(f"-- Table: {table_name}\n")

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