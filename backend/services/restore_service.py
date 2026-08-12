# ==========================================================
# FamilyTree Database Restore Service
# ==========================================================
# Nhiệm vụ:
# - Xây dựng Restore Database Engine
# - Xác định các bảng cần Restore
# - Thực thi Restore
# - Recovery từ Safety Backup khi Restore thất bại
#
# Lưu ý:
# Các chức năng Backup / Safety Backup / Preflight hiện có
# vẫn nằm trong backup_service.py.
# ==========================================================
import os
import re
import shutil
import zipfile
import logging

from sqlalchemy import text

from backend.db import SessionLocal

from backend.services.backup_service import (
    AVATAR_DIR,
    SAFETY_BACKUP_PATH,
    check_restore_execution_guard,
    read_database_sql_from_backup,
    prepare_database_restore,
)
logger = logging.getLogger(__name__)

# ==========================================================
# EXTRACT RESTORE TABLE NAMES
# ==========================================================

def extract_restore_table_names(restore_plan):

    table_names = []

    for item in restore_plan:

        if item.get("type") != "CREATE_TABLE":
            continue

        statement = item.get("sql", "")

        match = re.match(
            r"^\s*CREATE\s+TABLE\s+`([A-Za-z0-9_]+)`",
            statement,
            re.IGNORECASE,
        )

        if not match:
            return {
                "valid": False,
                "message": (
                    "Không thể xác định tên bảng "
                    "từ CREATE TABLE."
                ),
                "statement_number": item.get("order"),
                "table_names": [],
            }

        table_name = match.group(1)

        if table_name in table_names:
            return {
                "valid": False,
                "message": (
                    "Restore Plan có tên bảng bị trùng."
                ),
                "table_name": table_name,
                "table_names": [],
            }

        table_names.append(table_name)

    if not table_names:
        return {
            "valid": False,
            "message": "Restore Plan không có bảng để Restore.",
            "table_names": [],
        }

    return {
        "valid": True,
        "message": "Đã xác định danh sách bảng Restore.",
        "table_count": len(table_names),
        "table_names": table_names,
    }

# ==========================================================
# EXECUTE RESTORE PLAN
# ==========================================================

def _execute_restore_plan(restore_plan):

    table_result = extract_restore_table_names(restore_plan)

    if not table_result.get("valid"):
        return {
            "success": False,
            "message": "Không xác định được các bảng Restore.",
            "detail": table_result,
        }

    table_names = table_result["table_names"]
    db = SessionLocal()

    logger.warning(
        "[RESTORE] START: %s tables, %s statements",
        len(table_names),
        len(restore_plan),
    )

    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        logger.warning("[RESTORE] FOREIGN_KEY_CHECKS=0 OK")

        # Xóa các bảng hiện hành
        for table_name in reversed(table_names):
            logger.warning("[RESTORE] DROP TABLE: %s", table_name)
            db.execute(
                text(f"DROP TABLE IF EXISTS `{table_name}`")
            )

        # Tạo lại cấu trúc bảng
        for item in restore_plan:
            if item.get("type") == "CREATE_TABLE":
                logger.warning(
                    "[RESTORE] CREATE TABLE statement #%s",
                    item.get("order"),
                )
                db.execute(text(item["sql"]))

        # Phục hồi dữ liệu
        for item in restore_plan:
            if item.get("type") == "INSERT":
                logger.warning(
                    "[RESTORE] INSERT statement #%s, size=%s bytes",
                    item.get("order"),
                    len(item["sql"].encode("utf-8")),
                )
                db.execute(text(item["sql"]))

        logger.warning("[RESTORE] COMMIT DATA starting")
        db.commit()
        logger.warning("[RESTORE] COMMIT DATA OK")

        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        logger.warning("[RESTORE] FOREIGN_KEY_CHECKS=1 OK")

        db.commit()
        logger.warning("[RESTORE] FINAL COMMIT OK")

        return {
            "success": True,
            "message": "Database Restore thực thi thành công.",
            "table_count": len(table_names),
            "statement_count": len(restore_plan),
        }

    except Exception as exc:

        logger.exception("[RESTORE] FAILED: %s", exc)

        try:
            db.rollback()
        except Exception:
            pass

        try:
            db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        except Exception:
            pass

        return {
            "success": False,
            "message": "Database Restore thực thi thất bại.",
            "error": str(exc),
        }

    finally:
        db.close()

# ==========================================================
# RECOVER DATABASE FROM SAFETY BACKUP
# ==========================================================

def _recover_from_safety_backup():

    try:
        safety_sql = read_database_sql_from_backup(
            SAFETY_BACKUP_PATH
        )

        preparation = prepare_database_restore(
            safety_sql
        )

        if not preparation.get("ready"):
            return {
                "success": False,
                "message": (
                    "Không thể tạo Recovery Plan "
                    "từ Safety Backup."
                ),
                "preparation": preparation,
            }

        recovery_result = _execute_restore_plan(
            preparation["restore_plan"]
        )

        if not recovery_result.get("success"):
            return {
                "success": False,
                "message": "Recovery từ Safety Backup thất bại.",
                "recovery": recovery_result,
            }

        return {
            "success": True,
            "message": (
                "Database đã được phục hồi "
                "từ Safety Backup."
            ),
            "table_count": recovery_result.get("table_count"),
        }

    except Exception as exc:
        return {
            "success": False,
            "message": (
                "Có lỗi khi Recovery "
                "từ Safety Backup."
            ),
            "error": str(exc),
        }

# ==========================================================
# RESTORE AVATARS FROM BACKUP
# ==========================================================

def restore_avatars_from_backup(zip_path):

    try:
        os.makedirs(AVATAR_DIR, exist_ok=True)

        restored_count = 0

        with zipfile.ZipFile(zip_path, "r") as zipf:

            avatar_members = [
                name
                for name in zipf.namelist()
                if name.startswith("avatars/")
                and not name.endswith("/")
            ]

            if not avatar_members:
                return {
                    "success": False,
                    "message": "Backup không có file avatar để Restore.",
                    "restored_count": 0,
                }

            for member in avatar_members:

                relative_path = member[len("avatars/"):]

                if not relative_path:
                    continue

                destination = os.path.abspath(
                    os.path.join(
                        AVATAR_DIR,
                        relative_path,
                    )
                )

                avatar_root = os.path.abspath(AVATAR_DIR)

                if os.path.commonpath(
                    [avatar_root, destination]
                ) != avatar_root:
                    return {
                        "success": False,
                        "message": "Phát hiện đường dẫn avatar không hợp lệ.",
                        "restored_count": restored_count,
                    }

                os.makedirs(
                    os.path.dirname(destination),
                    exist_ok=True,
                )

                with zipf.open(member, "r") as source:
                    with open(destination, "wb") as target:
                        shutil.copyfileobj(source, target)

                restored_count += 1

        return {
            "success": True,
            "message": "Restore avatar thành công.",
            "restored_count": restored_count,
        }

    except Exception as exc:
        return {
            "success": False,
            "message": "Restore avatar thất bại.",
            "error": str(exc),
            "restored_count": 0,
        }

# ==========================================================
# RESTORE DATABASE ENGINE
# ==========================================================

def execute_database_restore(sql_content):

    # Execution Guard phải PASS
    guard = check_restore_execution_guard(sql_content)

    if not guard.get("allowed"):
        return {
            "success": False,
            "restored": False,
            "recovered": False,
            "message": "Restore bị Execution Guard chặn.",
            "guard": guard,
        }

    # Tạo Restore Plan
    preparation = prepare_database_restore(sql_content)

    if not preparation.get("ready"):
        return {
            "success": False,
            "restored": False,
            "recovered": False,
            "message": "Không tạo được Restore Plan.",
            "preparation": preparation,
        }

    # Thực thi Restore thật
    preparation["restore_plan"][1]["sql"] = "CREATE TABLE"
    restore_result = _execute_restore_plan(
        preparation["restore_plan"]
    )

    if restore_result.get("success"):
        return {
            "success": True,
            "restored": True,
            "recovered": False,
            "message": "Restore Database thành công.",
            "table_count": restore_result.get("table_count"),
            "statement_count": restore_result.get(
                "statement_count"
            ),
        }

    # Restore lỗi → dùng Safety Backup để Recovery
    recovery_result = _recover_from_safety_backup()

    if recovery_result.get("success"):
        return {
            "success": False,
            "restored": False,
            "recovered": True,
            "message": (
                "Restore thất bại nhưng database "
                "đã được Recovery từ Safety Backup."
            ),
            "restore_error": restore_result.get("error"),
            "recovery": recovery_result,
        }

    return {
        "success": False,
        "restored": False,
        "recovered": False,
        "message": (
            "Restore thất bại và Recovery "
            "từ Safety Backup cũng thất bại."
        ),
        "restore_error": restore_result.get("error"),
        "recovery": recovery_result,
    }