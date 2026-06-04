# ==========================================================
# File: backend/api/avatar.py
# Avatar V5 — Production Hardened
# ==========================================================

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.models.person_model import Person
import os
from backend.api.tree import TREE_CACHE
router = APIRouter()
# ✅ [DEBUG]: Kiểm tra avatar.py có được load không

# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_DIR = os.path.join(BASE_DIR, "static", "avatars")

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_MIME = {"image/jpeg": ".jpg", "image/png": ".png"}

os.makedirs(AVATAR_DIR, exist_ok=True)


# ==========================================================
# 📌 UPLOAD AVATAR
# ==========================================================
# ✅ [CHANGE 1]: Bỏ /api/avatar để dùng prefix từ main.py
@router.post("/upload/{person_id}")
async def upload_avatar(
    person_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # 1️⃣ MIME CHECK
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận JPG hoặc PNG")

    # 2️⃣ SIZE LIMIT
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File vượt quá 2MB")

    await file.seek(0)

    # 3️⃣ CHECK PERSON EXISTS
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.delete_status == 0
    ).first()

    if not person:
        raise HTTPException(status_code=404, detail="Không tìm thấy person")

    # 4️⃣ HASH RENAME
    ext = ALLOWED_MIME[file.content_type]
    filename = f"{person_id}{ext}"
    file_path = os.path.join(AVATAR_DIR, filename)

    # ✅ [CHANGE 2]: Xóa cả jpg + png cũ
    for ext in [".jpg", ".png"]:
        old_file = os.path.join(AVATAR_DIR, f"{person_id}{ext}")
        if os.path.exists(old_file):
            try:
                os.remove(old_file)
            except Exception:
                pass

    # 6️⃣ SAVE FILE
    tmp_path = file_path + ".tmp"

    with open(tmp_path, "wb") as f:
        f.write(contents)

    os.replace(tmp_path, file_path)

    # 7️⃣ UPDATE DB (ORM)
    from sqlalchemy.sql import func

    person.avatar = filename
    person.updated_at = func.now()
    db.commit()
    # Clear Tree cache để avatar mới hiện ngay
    TREE_CACHE.clear()
    return {
        "message": "Avatar uploaded successfully",
        "filename": filename
    }