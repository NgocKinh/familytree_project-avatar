# ==========================================================
# File: backend/api/avatar_cdn.py
# Avatar CDN — ORM Version (FINAL)
# ==========================================================

import os
import hashlib

from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.person_model import Person

router = APIRouter()

# ==========================================================
# CONFIG
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_DIR = os.path.join(BASE_DIR, "static", "avatars")

DEFAULT_MALE = os.path.join(AVATAR_DIR, "default_male.png")
DEFAULT_FEMALE = os.path.join(AVATAR_DIR, "default_female.png")
DEFAULT_OTHER = os.path.join(AVATAR_DIR, "default_other.png")


# ==========================================================
# FIND AVATAR FILE
# ==========================================================

def find_avatar(pid: int):
    for ext in ("png", "jpg"):
        path = os.path.join(AVATAR_DIR, f"{pid}.{ext}")
        if os.path.exists(path):
            return path
    return None


# ==========================================================
# DEFAULT AVATAR (ORM)
# ==========================================================

def default_avatar(pid: int, db: Session):

    person = db.query(Person).filter(
        Person.id == pid
    ).first()

    gender = (person.gender or "").strip().lower() if person else ""

    if gender == "male":
        return DEFAULT_MALE

    if gender == "female":
        return DEFAULT_FEMALE

    return DEFAULT_OTHER


# ==========================================================
# GENERATE ETAG
# ==========================================================

def compute_etag(path):
    stat = os.stat(path)
    key = f"{stat.st_mtime}-{stat.st_size}"
    return hashlib.md5(key.encode()).hexdigest()


# ==========================================================
# CDN AVATAR ENDPOINT
# ==========================================================

@router.get("/avatar/{pid}")
async def avatar(
    pid: int,
    request: Request,
    db: Session = Depends(get_db)
):

    # 1️⃣ tìm avatar thật
    path = find_avatar(pid)

    # 2️⃣ fallback default
    if not path:
        path = default_avatar(pid, db)

    # 3️⃣ tạo ETag
    etag = compute_etag(path)

    # 4️⃣ hỗ trợ 304 (cache browser)
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    # 5️⃣ trả file
    response = FileResponse(path)

    # 6️⃣ cache header (production ready)
    response.headers["Cache-Control"] = "public, max-age=86400"
    response.headers["ETag"] = etag

    return response