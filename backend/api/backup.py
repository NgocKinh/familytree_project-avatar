from fastapi import APIRouter
from backend.services.backup_service import (
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