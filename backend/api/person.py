# ==========================================================
#   file backend/api/person.py (ORM)
# ==========================================================
from backend.services import person_service
from backend.core.exceptions import NotFoundError
from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi import Request
from mysql.connector import Error
from backend.db_helper import get_connection, close_connection
import os
from datetime import datetime
# ===== ORM =====
from sqlalchemy.orm import Session
from fastapi import Depends
from backend.db import get_db
from backend.models.person_model import Person
from backend.schemas.person_schema import (
    PersonBasicResponse,
    PersonDetailResponse,
    PersonCreate
)
router = APIRouter()
# ==========================================================
# 🔧 CHUYỂN NGÀY MYSQL → ISO yyyy-mm-dd
# ==========================================================
def to_iso(date_value):
    """
    MySQL trả về kiểu datetime hoặc chuỗi GMT như:
        'Sat, 19 May 1956 00:00:00 GMT'
    Hàm này chuyển thành '1956-05-19'
    """
    if not date_value:
        return None

    # Nếu đã là yyyy-mm-dd → OK
    if (
        isinstance(date_value, str)
        and date_value[:4].isdigit()
        and date_value[4] == "-"
    ):
        return date_value[:10]

    try:
        # Parse chuỗi ngày GMT
        dt = datetime.strptime(str(date_value), "%a, %d %b %Y %H:%M:%S GMT")
        return dt.strftime("%Y-%m-%d")
    except:
        pass

    try:
        # datetime object
        return date_value.strftime("%Y-%m-%d")
    except:
        return None


# ==========================================================
# 🔧 AVATAR PATH SAFE (CHỈ TRẢ VỀ FILENAME)
# ==========================================================
def safe_avatar_file(gender, avatar_value, person_id=None):
    """
    Trả về ONLY filename:
        '5.jpg'
        hoặc 'default_male.png'
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(BASE_DIR, "static", "avatars")
    default_map = {
        "male": "default_male.png",
        "female": "default_female.png",
        "other": "default_other.png",
    }

    gen = (gender or "other").lower()
    val = str(avatar_value or "").strip()

    candidates = []

    if val:
        base = os.path.basename(val)
        candidates.append(base)

    if person_id:
        candidates.append(f"{person_id}.jpg")
        candidates.append(f"{person_id}.png")

    candidates.append(default_map.get(gen, "default_other.png"))

    for c in candidates:
        if os.path.exists(os.path.join(static_dir, c)):
            return c

    return default_map.get(gen, "default_other.png")

# ==========================================================
# 🆕 ORM - GET ALL PERSON
# ==========================================================
@router.get("/person", response_model=list[PersonBasicResponse])
def get_all_persons(db: Session = Depends(get_db)):
    return person_service.get_all_persons(db)

# ==========================================================
# 🆕 ORM - GET ONE PERSON
# ==========================================================
@router.get("/person/{pid}", response_model=PersonDetailResponse)
def get_person_orm(pid: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(
        Person.id == pid,
        Person.delete_status == 0
    ).first()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return person

# ==========================================================
# 🆕 ORM - CREATE PERSON
# ==========================================================
@router.post("/person", response_model=PersonDetailResponse)
def create_person(data: PersonCreate, db: Session = Depends(get_db)):
    return person_service.create_person(db, data)

@router.put("/person/{person_id}", response_model=PersonDetailResponse)
def update_person(person_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    try:
        return person_service.update_person(db, person_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

@router.delete("/person/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    try:
        person_service.delete_person(db, person_id)
        return {"message": "Deleted"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)        