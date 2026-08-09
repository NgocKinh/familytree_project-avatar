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
import shutil
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
# PERSISTENT SAFETY BACKUP DIRECTORY
# Railway Volume is mounted at:
# /app/backend/static/avatars
# ==========================================================

AVATAR_DIR = os.path.join(
    BASE_DIR,
    "static",
    "avatars"
)

SAFETY_BACKUP_DIR = os.path.join(
    AVATAR_DIR,
    "_safety_backup"
)

SAFETY_BACKUP_FILENAME = "TranAnQuan_SafetyBackup.zip"

SAFETY_BACKUP_PATH = os.path.join(
    SAFETY_BACKUP_DIR,
    SAFETY_BACKUP_FILENAME
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
# ANALYZE DATABASE SQL
# ==========================================================

def analyze_database_sql(sql_content):

    if not sql_content:
        return {
            "valid": False,
            "message": "database.sql rỗng.",
            "statements": [],
            "statement_count": 0,
        }

    statements = []
    current_statement = []

    for line in sql_content.splitlines():

        stripped = line.strip()

        # Bỏ dòng trống
        if not stripped:
            continue

        # Bỏ comment SQL dạng --
        if stripped.startswith("--"):
            continue

        current_statement.append(line)

        # File backup do FamilyTree tạo hiện dùng
        # dấu ; để kết thúc mỗi statement
        if stripped.endswith(";"):

            statement = "\n".join(
                current_statement
            ).strip()

            statements.append(statement)
            current_statement = []

    # Nếu cuối file còn SQL nhưng không có ;
    if current_statement:
        return {
            "valid": False,
            "message": "database.sql có câu lệnh SQL chưa kết thúc bằng dấu ;.",
            "statements": [],
            "statement_count": 0,
        }

    if not statements:
        return {
            "valid": False,
            "message": "Không tìm thấy câu lệnh SQL hợp lệ.",
            "statements": [],
            "statement_count": 0,
        }

    create_table_count = 0
    insert_count = 0
    set_count = 0
    other_count = 0

    for statement in statements:

        normalized = statement.lstrip().upper()

        if normalized.startswith("CREATE TABLE"):
            create_table_count += 1

        elif normalized.startswith("INSERT INTO"):
            insert_count += 1

        elif normalized.startswith("SET "):
            set_count += 1

        else:
            other_count += 1

    return {
        "valid": True,
        "message": "database.sql đã được đọc và phân tích thành công.",
        "statements": statements,
        "statement_count": len(statements),
        "create_table_count": create_table_count,
        "insert_count": insert_count,
        "set_count": set_count,
        "other_count": other_count,
    }

# ==========================================================
# PREFLIGHT DATABASE SQL
# ==========================================================

def preflight_database_sql(sql_content):

    analysis = analyze_database_sql(sql_content)

    if not analysis.get("valid"):
        return analysis

    # Backup FamilyTree hiện chỉ được phép chứa:
    # SET ...
    # CREATE TABLE ...
    # INSERT INTO ...
    if analysis.get("other_count", 0) != 0:
        return {
            "valid": False,
            "message": "database.sql chứa câu lệnh không được phép.",
            "statement_count": analysis.get("statement_count", 0),
            "other_count": analysis.get("other_count", 0),
        }

    # Một backup database hợp lệ phải có cấu trúc bảng
    if analysis.get("create_table_count", 0) == 0:
        return {
            "valid": False,
            "message": "database.sql không có câu lệnh CREATE TABLE.",
            "statement_count": analysis.get("statement_count", 0),
        }

    # Kiểm tra dấu hiệu nhận dạng của backup FamilyTree
    required_tables = {
        "person",
        "users",
        "parent_child",
        "marriage",
    }

    create_statements = [
        statement
        for statement in analysis["statements"]
        if statement.lstrip().upper().startswith("CREATE TABLE")
    ]

    missing_tables = []

    for table_name in required_tables:

        expected = f"CREATE TABLE `{table_name}`".upper()

        found = any(
            statement.lstrip().upper().startswith(expected)
            for statement in create_statements
        )

        if not found:
            missing_tables.append(table_name)

    if missing_tables:
        return {
            "valid": False,
            "message": "database.sql thiếu bảng bắt buộc của FamilyTree.",
            "missing_tables": missing_tables,
        }

    return {
        "valid": True,
        "message": "Preflight database.sql PASS.",
        "statement_count": analysis["statement_count"],
        "create_table_count": analysis["create_table_count"],
        "insert_count": analysis["insert_count"],
        "set_count": analysis["set_count"],
        "other_count": analysis["other_count"],
    }

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
    os.makedirs(
        SAFETY_BACKUP_DIR,
        exist_ok=True
    )

    # Copy bản mới vào chính Railway Volume trước.
    # Không ghi đè Safety Backup cũ khi copy chưa hoàn tất.
    safety_temp_path = SAFETY_BACKUP_PATH + ".tmp"

    shutil.copy2(
        backup_path,
        safety_temp_path
    )

    # Kiểm tra lại bản đã copy trên Volume
    volume_validation = validate_restore_zip(
        safety_temp_path
    )

    if not volume_validation.get("valid"):

        if os.path.exists(safety_temp_path):
            os.remove(safety_temp_path)

        if os.path.exists(backup_path):
            os.remove(backup_path)

        return {
            "success": False,
            "message": "Safety Backup trên Volume không hợp lệ.",
            "filename": None,
            "validation": volume_validation,
        }

    # Bản .tmp đã PASS.
    # Hai file này cùng nằm trên Railway Volume,
    # nên os.replace có thể thay bản cũ an toàn.
    os.replace(
        safety_temp_path,
        SAFETY_BACKUP_PATH
    )

    # File backup tạm ở filesystem container không cần giữ lại
    if os.path.exists(backup_path):
        os.remove(backup_path)

    return {
        "success": True,
        "message": "Safety Backup đã được tạo và kiểm tra thành công.",
        "filename": SAFETY_BACKUP_FILENAME,
        "validation": validation,
    }

# ==========================================================
# CHECK SAFETY BACKUP
# ==========================================================

def check_safety_backup():

    if not os.path.isfile(SAFETY_BACKUP_PATH):
        return {
            "valid": False,
            "message": "Không tìm thấy Safety Backup.",
            "filename": SAFETY_BACKUP_FILENAME,
        }

    validation = validate_restore_zip(
        SAFETY_BACKUP_PATH
    )

    if not validation.get("valid"):
        return {
            "valid": False,
            "message": "Safety Backup không hợp lệ.",
            "filename": SAFETY_BACKUP_FILENAME,
            "validation": validation,
        }

    return {
        "valid": True,
        "message": "Safety Backup tồn tại và hợp lệ.",
        "filename": SAFETY_BACKUP_FILENAME,
        "validation": validation,
    }