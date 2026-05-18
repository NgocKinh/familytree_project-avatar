# ==========================================================
# File: backend/api/marriage.py
# Version: v2.0 - Return full spouse name fields for formatName
# ==========================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from datetime import datetime

from backend.db import get_db
from backend.models.marriage_model import Marriage

from backend.schemas.marriage_schema import MarriageCreate, MarriageUpdate
from backend.services.marriage_service import create_marriage
from backend.db import get_connection
router = APIRouter(tags=["Marriage"])

# ==========================================================
# 🔵 [ADDED]: Helper trả dữ liệu người đầy đủ cho formatName frontend
# ==========================================================
def person_payload(person):
    if not person:
        return None

    return {
        "id": getattr(person, "id", None),
        "sur_name": getattr(person, "sur_name", "") or "",
        "last_name": getattr(person, "last_name", "") or "",
        "middle_name": getattr(person, "middle_name", "") or "",
        "first_name": getattr(person, "first_name", "") or "",

        # tên hiệu / tên gọi khác nếu DB có cột này thì tự lấy, chưa có thì rỗng
        "alias_name": (
            getattr(person, "alias_name", None)
            or getattr(person, "nick_name", None)
            or getattr(person, "other_name", None)
            or ""
        ),

        "gender": getattr(person, "gender", None),
        "birth_date": getattr(person, "birth_date", None),
        "death_date": getattr(person, "death_date", None),
    }


# ==========================================================
# 🔵 [ADDED]: Helper giữ tương thích spouse_a_name / spouse_b_name cũ
# ==========================================================
def simple_full_name(person):
    if not person:
        return ""

    parts = [
        getattr(person, "sur_name", "") or "",
        getattr(person, "last_name", "") or "",
        getattr(person, "middle_name", "") or "",
        getattr(person, "first_name", "") or "",
    ]

    return " ".join([p.strip() for p in parts if p and p.strip()])


# ==========================================================
# 🔵 [ADDED]: Helper đóng gói marriage cho frontend
# ==========================================================
def marriage_payload(m):
    priority = getattr(m, "priority", 0) or 0
    return {
        "id": m.id,
        "spouse_a_id": m.spouse_a_id,
        "spouse_b_id": m.spouse_b_id,

        # giữ field cũ để MarriageList chưa hư
        "spouse_a_name": simple_full_name(m.spouse_a),
        "spouse_b_name": simple_full_name(m.spouse_b),

        # field mới để dùng formatName chuẩn
        "spouse_a": person_payload(m.spouse_a),
        "spouse_b": person_payload(m.spouse_b),

        "start_date": m.start_date,
        "end_date": m.end_date,
        "status": m.status,
        "computed_status": getattr(m, "computed_status", None) or m.status,
        "ceremony_type": m.ceremony_type,
        "location": m.location,
        "notes": m.notes,
        "consanguineous": bool(m.consanguineous),
        "allow_underage": bool(getattr(m, "allow_underage", False)),
        "priority": priority,
    }

# ==========================================================
# CREATE MARRIAGE
# ==========================================================
@router.post("", status_code=status.HTTP_201_CREATED)
def create_marriage_api(data: MarriageCreate, db: Session = Depends(get_db)):
    return create_marriage(db, data)


# ==========================================================
# ✅ [CHANGE 1]: GET ALL MARRIAGES trả thêm spouse_a / spouse_b đầy đủ
# ==========================================================
@router.get("")
def get_all_marriages(db: Session = Depends(get_db)):
    marriages = (
        db.query(Marriage)
        .options(
            joinedload(Marriage.spouse_a),
            joinedload(Marriage.spouse_b),
        )
        .all()
    )

    result = [marriage_payload(m) for m in marriages]



    return result
    
# ==========================================================
# ✅ [CHANGE 2]: endpoint detail đúng theo Swagger hiện tại
# /api/marriage/detail/{mid}
# ==========================================================
@router.get("/detail/{mid}")
def get_marriage_detail(mid: int, db: Session = Depends(get_db)):
    marriage = (
        db.query(Marriage)
        .options(
            joinedload(Marriage.spouse_a),
            joinedload(Marriage.spouse_b),
        )
        .filter(Marriage.id == mid)
        .first()
    )

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    return marriage_payload(marriage)


# ==========================================================
# GET ONE MARRIAGE - giữ route cũ nếu frontend còn dùng
# ==========================================================
@router.get("/{mid}")
def get_marriage(mid: int, db: Session = Depends(get_db)):
    marriage = (
        db.query(Marriage)
        .options(
            joinedload(Marriage.spouse_a),
            joinedload(Marriage.spouse_b),
        )
        .filter(Marriage.id == mid)
        .first()
    )

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    return marriage_payload(marriage)


# ==========================================================
# UPDATE MARRIAGE
# ==========================================================
@router.put("/{mid}")
def update_marriage(mid: int, data: MarriageUpdate, db: Session = Depends(get_db)):
    marriage = db.query(Marriage).filter(Marriage.id == mid).first()

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(marriage, key, value)

    if "status" in update_data:
        marriage.status_changed_at = datetime.utcnow()

    db.commit()
    db.refresh(marriage)

    return marriage_payload(marriage)


# ==========================================================
# DELETE MARRIAGE
# ==========================================================
@router.delete("/{mid}")
def delete_marriage(mid: int, db: Session = Depends(get_db)):
    marriage = db.query(Marriage).filter(Marriage.id == mid).first()

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    db.delete(marriage)
    db.commit()

    return {"message": "Deleted successfully"}


# ==========================================================
# GET ALL MARRIAGES OF A PERSON
# ==========================================================
@router.get("/person/{person_id}")
def get_person_marriages(person_id: int, db: Session = Depends(get_db)):
    marriages = (
        db.query(Marriage)
        .options(
            joinedload(Marriage.spouse_a),
            joinedload(Marriage.spouse_b),
        )
        .filter(
            or_(
                Marriage.spouse_a_id == person_id,
                Marriage.spouse_b_id == person_id,
            )
        )
        .all()
    )

    result = []

    for m in marriages:
        partner = m.spouse_b if m.spouse_a_id == person_id else m.spouse_a

        result.append({
            "marriage_id": m.id,
            "partner_id": getattr(partner, "id", None) if partner else None,
            "partner": person_payload(partner),
            "status": m.status,
        })

    return result

# ==========================================================
# UPDATE PRIORITY
# ==========================================================
@router.put("/{mid}/priority")
def update_priority(mid: int, data: dict, db: Session = Depends(get_db)):

    priority = int(data.get("priority", 0))

    marriage = (
        db.query(Marriage)
        .filter(Marriage.id == mid)
        .first()
    )

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    marriage.priority = priority

    db.commit()
    db.refresh(marriage)



    return {
        "success": True
    }