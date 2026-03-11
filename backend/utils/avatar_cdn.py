import os
import hashlib

from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse

from backend.db_helper import get_connection, close_connection

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_DIR = os.path.join(BASE_DIR, "static", "avatars")

DEFAULT_MALE = os.path.join(AVATAR_DIR, "default_male.png")
DEFAULT_FEMALE = os.path.join(AVATAR_DIR, "default_female.png")
DEFAULT_OTHER = os.path.join(AVATAR_DIR, "default_other.png")


# ----------------------------------------------------------
# FIND AVATAR FILE
# ----------------------------------------------------------

def find_avatar(pid: int):

    for ext in ("jpg", "png", "webp"):
        path = os.path.join(AVATAR_DIR, f"{pid}.{ext}")

        if os.path.exists(path):
            return path

    return None


# ----------------------------------------------------------
# GET DEFAULT AVATAR FROM DB GENDER
# ----------------------------------------------------------

def default_avatar(pid):

    from backend.db_helper import get_connection, close_connection

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT gender FROM person WHERE person_id=%s",
        (pid,)
    )

    row = cursor.fetchone()

    close_connection(conn, cursor)

    gender = ""

    if row and row.get("gender"):
        gender = str(row["gender"]).strip().lower()

    print("DEBUG PID:", pid, "GENDER:", gender)

    if gender == "male":
        return DEFAULT_MALE

    if gender == "female":
        return DEFAULT_FEMALE

    return DEFAULT_OTHER


# ----------------------------------------------------------
# GENERATE ETAG
# ----------------------------------------------------------

def compute_etag(path):

    stat = os.stat(path)

    key = f"{stat.st_mtime}-{stat.st_size}"

    return hashlib.md5(key.encode()).hexdigest()


# ----------------------------------------------------------
# CDN AVATAR ENDPOINT
# ----------------------------------------------------------

@router.get("/avatar/{pid}")
async def avatar(pid: int, request: Request):

    path = find_avatar(pid)

    if not path:
        path = default_avatar(pid)

    etag = compute_etag(path)

    # DEV: disable 304 cache
    # if request.headers.get("if-none-match") == etag:
    #     return Response(status_code=304)

    response = FileResponse(path)

    # TODO response.headers["Cache-Control"] = "public, max-age=31536000"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["ETag"] = etag

    return response