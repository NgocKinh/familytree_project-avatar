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
from backend.models.marriage_model import Marriage
from backend.models.parent_child_model import ParentChild
from backend.schemas.person_schema import (
    PersonBasicResponse,
    PersonDetailResponse,
    PersonCreate
)
from backend.schemas.person_schema import (
    BirthOrderBulkUpdate
)
router = APIRouter(tags=["Person"])

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
# ✅ [CHANGE 1]: Trả thêm delete_status cho frontend
@router.get("/")
def get_all_persons(db: Session = Depends(get_db)):
    persons = person_service.get_all_persons(db)

    return [
        {
            "id": p.id,
            "sur_name": p.sur_name,
            "last_name": p.last_name,
            "middle_name": p.middle_name,
            "first_name": p.first_name,
            "gender": p.gender,
            "birth_date": str(p.birth_date) if p.birth_date else None,
            "death_date": str(p.death_date) if p.death_date else None,

            # 🔥 QUAN TRỌNG NHẤT
            "delete_status": getattr(p, "delete_status", 0)
        }
        for p in persons
    ]
# ===============================
# SOFT DELETE
# ===============================
@router.put("/delete_soft/{person_id}")
def soft_delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    # ==========================================================
    # 🔒 DEPENDENCY INSPECTOR
    # ==========================================================

    marriage_count = db.query(Marriage).filter(
        (Marriage.spouse_a_id == person_id) |
        (Marriage.spouse_b_id == person_id)
    ).count()

    parent_child_count = db.query(ParentChild).filter(
        (ParentChild.parent_id == person_id) |
        (ParentChild.child_id == person_id)
    ).count()

    if marriage_count > 0 or parent_child_count > 0:

        messages = []

        if marriage_count > 0:
            messages.append(f"Còn {marriage_count} quan hệ hôn nhân")

        if parent_child_count > 0:
            messages.append(f"Còn {parent_child_count} quan hệ cha-con")

        raise HTTPException(
            status_code=400,
            detail={
                "message": "Không thể tạm ẩn thành viên này",
                "details": messages
            }
        )
        
    person.delete_status = 1
    db.commit()

    return {"success": True}

# ===============================
# RESTORE
# ===============================
@router.put("/restore/{person_id}")
def restore_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    person.delete_status = 0
    db.commit()

    return {"success": True}


# ===============================
# HARD DELETE
# ===============================
@router.delete("/delete_permanent/{person_id}")
def hard_delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.commit()

    return {"success": True}
# ==========================================================
# 🆕 ORM - GET ONE PERSON
# ==========================================================
@router.get("/{pid}")
def get_person_orm(pid: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(
        Person.id == pid
    ).first()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return {
        "id": person.id,
        "sur_name": person.sur_name,
        "last_name": person.last_name,
        "middle_name": person.middle_name,
        "first_name": person.first_name,
        "gender": person.gender,
        "birth_date": str(person.birth_date) if person.birth_date else None,
        "birth_order": person.birth_order,
        "death_date": str(person.death_date) if person.death_date else None,
        "anniversary_death": person.anniversary_death,
        "anniversary_type": person.anniversary_type,
        "birth_date_precision": person.birth_date_precision,
        "death_date_precision": person.death_date_precision
    }

# ==========================================================
# 🆕 ORM - CREATE PERSON
# ==========================================================
@router.post("/", response_model=PersonDetailResponse)
def create_person(data: PersonCreate, db: Session = Depends(get_db)):
    return person_service.create_person(db, data)

@router.put("/{person_id}", response_model=PersonDetailResponse)
def update_person(person_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    try:
        return person_service.update_person(db, person_id, payload)
    except NotFoundError as e:

        raise HTTPException(status_code=404, detail=e.message)

@router.delete("/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    try:
        person_service.delete_person(db, person_id)
        return {"message": "Deleted"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
# ==========================================================
# BULK UPDATE BIRTH ORDER
# ==========================================================
@router.put("/birth-order/bulk")
def update_birth_order_bulk(
    payload: BirthOrderBulkUpdate,
    db: Session = Depends(get_db)
):

    for item in payload.items:

        person = db.query(Person).filter(
            Person.id == item.person_id
        ).first()

        if not person:
            continue

        person.birth_order = item.birth_order

    db.commit()

    return {
        "success": True,
        "message": "Birth Order updated successfully"
    }
# ==========================================================
# CHECK DUPLICATE
# ==========================================================
@router.post("/check_duplicate")
def check_duplicate(data: dict):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            person_id,
            sur_name,
            last_name,
            middle_name,
            first_name,
            gender,
            birth_date,
            death_date
        FROM persons
        WHERE
            last_name = %s
            AND first_name = %s
            AND gender = %s
    """, (
        data.get("last_name"),
        data.get("first_name"),
        data.get("gender"),
    ))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {
        "duplicate": len(rows) > 0,
        "matches": rows
    }