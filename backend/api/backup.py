from fastapi import APIRouter
from fastapi.responses import FileResponse

import os

from backend.services.backup_service import (
    BACKUP_DIR,
    create_backup_zip
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