from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import FileResponse

import os
import tempfile

from backend.api.auth import get_current_user
from backend.models.user_model import User
from backend.services.backup_service import (
    BACKUP_DIR,
    create_backup_zip,
    list_backup_files,
    validate_restore_zip,
    create_safety_backup,
    check_safety_backup,
    read_database_sql_from_backup,
    preflight_database_sql,
    prepare_database_restore,
    check_restore_execution_guard,
    prepare_safety_backup_recovery,
)
from backend.services.restore_service import (
    execute_database_restore,
    restore_avatars_from_backup,
)

def require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới có quyền phục hồi dữ liệu",
        )

router = APIRouter(
    prefix="/api/backup",
    tags=["Backup"]
)

@router.post("/create")
def create_backup():

    filename = create_backup_zip()

    return {
        "success": True,
        "message": "Backup created successfully.",
        "filename": filename
    }

@router.get("/list")
def list_backups():

    return {
        "success": True,
        "files": list_backup_files()
    }
    
@router.get("/download/{filename}")
def download_backup(filename: str):

    filepath = os.path.join(
        BACKUP_DIR,
        filename
    )

    return FileResponse(
        filepath,
        filename=filename,
        media_type="application/zip"
    )

@router.post("/restore/validate")
async def validate_restore(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Chỉ chấp nhận file ZIP",
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
    ) as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        result = validate_restore_zip(temp_path)
        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/restore/preflight")
async def preflight_restore(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Chỉ chấp nhận file ZIP",
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
    ) as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        # Bước 1: kiểm tra cấu trúc ZIP
        zip_validation = validate_restore_zip(temp_path)

        if not zip_validation.get("valid"):
            raise HTTPException(
                status_code=400,
                detail=zip_validation,
            )

        # Bước 2: chỉ đọc database.sql
        sql_content = read_database_sql_from_backup(
            temp_path
        )

        # Bước 3: phân tích + preflight
        preflight = preflight_database_sql(
            sql_content
        )

        if not preflight.get("valid"):
            raise HTTPException(
                status_code=400,
                detail=preflight,
            )

        return {
            "success": True,
            "message": "Restore preflight PASS.",
            "zip_validation": zip_validation,
            "database_preflight": preflight,
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/restore/prepare")
async def prepare_restore(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Chỉ chấp nhận file ZIP",
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
    ) as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        # Bước 1: Validate ZIP
        zip_validation = validate_restore_zip(temp_path)

        if not zip_validation.get("valid"):
            raise HTTPException(
                status_code=400,
                detail=zip_validation,
            )

        # Bước 2: Đọc database.sql
        sql_content = read_database_sql_from_backup(
            temp_path
        )

        # Bước 3: Tạo Restore Plan
        preparation = prepare_database_restore(
            sql_content
        )

        if not preparation.get("ready"):
            raise HTTPException(
                status_code=400,
                detail=preparation,
            )

        # Chỉ thống kê plan.
        # Tuyệt đối không trả nội dung SQL ra API.
        type_counts = {
            "SET": 0,
            "CREATE_TABLE": 0,
            "INSERT": 0,
        }

        for item in preparation["restore_plan"]:
            statement_type = item["type"]

            if statement_type in type_counts:
                type_counts[statement_type] += 1

        return {
            "success": True,
            "ready": True,
            "message": "Database Restore Prepare PASS.",
            "statement_count": preparation["statement_count"],
            "type_counts": type_counts,
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/restore/execution-guard")
async def restore_execution_guard(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Chỉ chấp nhận file ZIP",
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
    ) as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        zip_validation = validate_restore_zip(temp_path)

        if not zip_validation.get("valid"):
            raise HTTPException(
                status_code=400,
                detail=zip_validation,
            )

        sql_content = read_database_sql_from_backup(
            temp_path
        )

        guard = check_restore_execution_guard(
            sql_content
        )

        if not guard.get("allowed"):
            raise HTTPException(
                status_code=409,
                detail=guard,
            )

        return {
            "success": True,
            "allowed": True,
            "message": "Restore Execution Guard PASS.",
            "safety_backup": guard["safety_backup"],
            "statement_count": guard["statement_count"],
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/restore/recovery/prepare")
def prepare_restore_recovery(
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    recovery = prepare_safety_backup_recovery()

    if not recovery.get("ready"):
        raise HTTPException(
            status_code=409,
            detail=recovery,
        )

    return {
        "success": True,
        "ready": True,
        "message": recovery["message"],
        "filename": recovery["filename"],
        "statement_count": recovery["statement_count"],
        "type_counts": recovery["type_counts"],
    }

@router.post("/restore/execute")
async def execute_restore(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(
            status_code=400,
            detail="Chỉ chấp nhận file ZIP",
        )

    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".zip",
    ) as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        zip_validation = validate_restore_zip(temp_path)

        if not zip_validation.get("valid"):
            raise HTTPException(
                status_code=400,
                detail=zip_validation,
            )

        sql_content = read_database_sql_from_backup(
            temp_path
        )

        result = execute_database_restore(
            sql_content
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=409,
                detail=result,
            )

        avatar_result = restore_avatars_from_backup(
            temp_path
        )

        if not avatar_result.get("success"):
            raise HTTPException(
                status_code=409,
                detail={
                    "success": False,
                    "message": (
                        "Database Restore thành công "
                        "nhưng Avatar Restore thất bại."
                    ),
                    "database_restore": result,
                    "avatar_restore": avatar_result,
                },
            )

        result["avatar_restore"] = avatar_result

        return result

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/restore/safety-backup")
def create_restore_safety_backup(
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    result = create_safety_backup()

    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result,
        )

    return result

@router.get("/restore/safety-backup/check")
def check_restore_safety_backup(
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    result = check_safety_backup()

    if not result.get("valid"):
        raise HTTPException(
            status_code=409,
            detail=result,
        )

    return result