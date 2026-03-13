# ==========================================================
# File: backend/api/avatar.py
# Avatar V5 — Production Hardened
# ==========================================================

from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.db_helper import get_connection, close_connection
import os
import uuid

router = APIRouter()

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
@router.post("/api/person/{person_id}/avatar")
async def upload_avatar(person_id: int, file: UploadFile = File(...)):

    # 1️⃣ MIME CHECK
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận JPG hoặc PNG")

    # 2️⃣ SIZE LIMIT
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File vượt quá 2MB")

    await file.seek(0)

    # 3️⃣ CHECK PERSON EXISTS
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT person_id FROM person WHERE person_id=%s AND delete_status=0",
            (person_id,),
        )

        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy person")

    finally:
        close_connection(conn, cursor)

    # 4️⃣ HASH RENAME
    ext = ALLOWED_MIME[file.content_type]
    filename = f"{person_id}{ext}"
    file_path = os.path.join(AVATAR_DIR, filename)

    # 5️⃣ REMOVE OLD AVATAR + SAVE FILE + UPDATE DB
    conn, cursor = None, None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # lấy avatar cũ
        cursor.execute(
            "SELECT avatar FROM person WHERE person_id=%s",
            (person_id,),
        )
        row = cursor.fetchone()

        # xóa avatar cũ
        if row and row.get("avatar") and row["avatar"] != filename:
            old_file = os.path.join(AVATAR_DIR, row["avatar"])
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                except Exception:
                    pass

        # lưu avatar mới
        tmp_path = file_path + ".tmp"

        with open(tmp_path, "wb") as f:
            f.write(contents)

        os.replace(tmp_path, file_path)

        # update database
        cursor.execute(
            "UPDATE person SET avatar=%s, updated_at=NOW() WHERE person_id=%s",
            (filename, person_id),
        )

        conn.commit()

    finally:
        close_connection(conn, cursor)

    return {
        "message": "Avatar uploaded successfully",
        "filename": filename
    }