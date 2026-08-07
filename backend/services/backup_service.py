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
from datetime import datetime
import zipfile

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
# CREATE EMPTY BACKUP
# ==========================================================

def create_backup_file():

    ensure_backup_dir()

    filename = generate_backup_filename()

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    with zipfile.ZipFile(
        filepath,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        zipf.writestr(
            "README.txt",
            "FamilyTree Backup\n"
        )

        zipf.writestr(
            "version.txt",
            "FamilyTree Version 1.0\n"
        )

    return filename