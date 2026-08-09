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
from zoneinfo import ZoneInfo

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

        avatar_dir = os.path.join(
            BASE_DIR,
            "static",
            "avatars"
        )

        if os.path.isdir(avatar_dir):

            for root, dirs, files in os.walk(avatar_dir):

                for avatar_file in files:

                    avatar_path = os.path.join(
                        root,
                        avatar_file
                    )

                    relative_path = os.path.relpath(
                        avatar_path,
                        avatar_dir
                    )

                    zip_path = os.path.join(
                        "avatars",
                        relative_path
                    )

                    zipf.write(
                        avatar_path,
                        zip_path
                    )

        readme_content = (
            "FAMILYTREE BACKUP\n"
            "=================\n\n"
            "Đây là file sao lưu dữ liệu của hệ thống FamilyTree.\n\n"
            "NỘI DUNG BACKUP\n"
            "---------------\n"
            "- database.sql : Dữ liệu cơ sở dữ liệu MySQL.\n"
            "- avatars/     : Ảnh đại diện của các thành viên.\n"
            "- README.txt   : Hướng dẫn về file backup.\n"
            "- version.txt  : Thông tin phiên bản backup.\n\n"
            "LƯU Ý\n"
            "------\n"
            "- Không chỉnh sửa trực tiếp database.sql nếu không hiểu rõ cấu trúc dữ liệu.\n"
            "- Không đổi tên hoặc xóa các file trong thư mục avatars.\n"
            "- Nên lưu file backup ở nơi an toàn.\n"
            "- Việc phục hồi dữ liệu nên được thực hiện bởi người quản trị hệ thống.\n"
        )

        zipf.writestr(
            "README.txt",
            readme_content
        )

        vietnam_time = datetime.now(
            ZoneInfo("Asia/Ho_Chi_Minh")
        )

        version_content = (
            "FAMILYTREE BACKUP VERSION\n"
            "=========================\n\n"
            "Backup Format Version: 1.0\n"
            "Project: FamilyTree\n"
            "Database: MySQL\n"
            f"Created: {vietnam_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            "Timezone: Asia/Ho_Chi_Minh (UTC+7)\n"
        )

        zipf.writestr(
            "version.txt",
            version_content
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

# ==========================================================
# VALIDATE RESTORE ZIP
# ==========================================================

def validate_restore_zip(zip_path):

    required_files = {
        "database.sql",
        "README.txt",
        "version.txt",
    }

    try:
        with zipfile.ZipFile(zip_path, "r") as zipf:

            names = zipf.namelist()

            missing_files = [
                required_file
                for required_file in required_files
                if required_file not in names
            ]

            has_avatars = any(
                name.startswith("avatars/")
                for name in names
            )

            if missing_files:
                return {
                    "valid": False,
                    "message": "Backup thiếu file bắt buộc.",
                    "missing_files": missing_files,
                }

            if not has_avatars:
                return {
                    "valid": False,
                    "message": "Backup thiếu thư mục avatars.",
                    "missing_files": ["avatars/"],
                }

            return {
                "valid": True,
                "message": "File backup hợp lệ.",
                "missing_files": [],
            }

    except zipfile.BadZipFile:
        return {
            "valid": False,
            "message": "File không phải ZIP hợp lệ.",
            "missing_files": [],
        }
            
# ==========================================================
# READ DATABASE SQL FROM BACKUP
# ==========================================================

def read_database_sql_from_backup(zip_path):

    with zipfile.ZipFile(zip_path, "r") as zipf:

        if "database.sql" not in zipf.namelist():
            raise ValueError(
                "Backup không có file database.sql"
            )

        sql_bytes = zipf.read("database.sql")

        return sql_bytes.decode("utf-8")

# ==========================================================
# CREATE + VALIDATE SAFETY BACKUP
# ==========================================================

def create_safety_backup():

    # Tạo backup đầy đủ của trạng thái hiện tại
    backup_filename = create_backup_zip()

    backup_path = os.path.join(
        BACKUP_DIR,
        backup_filename
    )

    # Kiểm tra backup vừa tạo trước khi cho phép Restore
    validation = validate_restore_zip(backup_path)

    if not validation.get("valid"):

        if os.path.exists(backup_path):
            os.remove(backup_path)

        return {
            "success": False,
            "message": "Không thể tạo Safety Backup hợp lệ.",
            "filename": None,
            "validation": validation,
        }

    # Tên cố định giúp hệ thống chỉ duy trì
    # một Safety Backup hiện hành
    safety_filename = "TranAnQuan_SafetyBackup.zip"

    safety_path = os.path.join(
        BACKUP_DIR,
        safety_filename
    )

    # Chỉ thay Safety Backup cũ SAU KHI
    # backup mới đã được tạo và validate thành công
    os.replace(
        backup_path,
        safety_path
    )

    return {
        "success": True,
        "message": "Safety Backup đã được tạo và kiểm tra thành công.",
        "filename": safety_filename,
        "validation": validation,
    }

# ==========================================================
# CHECK SAFETY BACKUP
# ==========================================================

def check_safety_backup():

    safety_filename = "TranAnQuan_SafetyBackup.zip"

    safety_path = os.path.join(
        BACKUP_DIR,
        safety_filename
    )

    if not os.path.isfile(safety_path):
        return {
            "valid": False,
            "message": "Không tìm thấy Safety Backup.",
            "filename": safety_filename,
        }

    validation = validate_restore_zip(safety_path)

    if not validation.get("valid"):
        return {
            "valid": False,
            "message": "Safety Backup không hợp lệ.",
            "filename": safety_filename,
            "validation": validation,
        }

    return {
        "valid": True,
        "message": "Safety Backup tồn tại và hợp lệ.",
        "filename": safety_filename,
        "validation": validation,
    }