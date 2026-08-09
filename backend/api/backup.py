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