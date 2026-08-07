from fastapi import APIRouter
from backend.services.backup_service import (
    ensure_backup_dir,
    generate_backup_filename
)

router = APIRouter(
    prefix="/api/backup",
    tags=["Backup"]
)


# ==========================================================
# CREATE BACKUP
# ==========================================================

@router.post("/create")
def create_backup():

    ensure_backup_dir()

    filename = generate_backup_filename()

    return {
        "success": True,
        "message": "Backup service is ready.",
        "filename": filename
    }