from fastapi import APIRouter, Depends, HTTPException
from backend.core.exceptions import BadRequestException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from typing import List
from backend.db import get_db
from backend.schemas.marriage_schema import MarriageCreate, MarriageResponse, MarriageUpdate
from backend.models.marriage_model import Marriage

from backend.services.marriage_service import (
    create_marriage,
    get_display_marriage,
    build_marriage_response,
    get_all_marriages,
    get_marriage_by_id,
    end_marriage,
    build_marriage_timeline
)
from datetime import date
from typing import Optional

router = APIRouter(tags=["Marriage"])

# ==========================================================
# 🔵 [ADDED]: Helper trả người đầy đủ cho formatName frontend
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
        "gender": getattr(person, "gender", None),
        "birth_date": getattr(person, "birth_date", None),
        "death_date": getattr(person, "death_date", None),
    }


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


def marriage_payload(m):
    return {
        "id": m.id,
        "spouse_a_id": m.spouse_a_id,
        "spouse_b_id": m.spouse_b_id,

        "spouse_a_name": simple_full_name(m.spouse_a),
        "spouse_b_name": simple_full_name(m.spouse_b),

        "spouse_a": person_payload(m.spouse_a),
        "spouse_b": person_payload(m.spouse_b),

        "start_date": m.start_date,
        "end_date": m.end_date,
        "status": m.status,
        "computed_status": getattr(m, "computed_status", None) or m.status,
        "ceremony_type": m.ceremony_type,
        "location": m.location,
        "notes": m.notes,
        "consanguineous": bool(getattr(m, "consanguineous", False)),
        "allow_underage": bool(getattr(m, "allow_underage", False)),
    }
# ==========================================================
# CREATE MARRIAGE
# ==========================================================
@router.post("/", response_model=MarriageResponse)
def create(data: MarriageCreate, db: Session = Depends(get_db)):
    try:
        marriage = create_marriage(db, data)
        return build_marriage_response(marriage)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Database constraint violated")
# ==========================================================
# END MARRIAGE
# ==========================================================
@router.post("/end")
def end_marriage_api(
    marriage_id: int,
    reason: str,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    return build_marriage_response(
    end_marriage(db, marriage_id, reason, end_date)
)
# ==========================================================
# PATCH MARRIAGE (UPDATE STATUS / GET / END DATE)
# ==========================================================
@router.patch("/{marriage_id}", response_model=MarriageResponse)
def update_marriage_api(
    marriage_id: int,
    data: MarriageUpdate,
    db: Session = Depends(get_db)
):
    try:
        updated = end_marriage(
            db,
            marriage_id=marriage_id,
            reason=data.status,
            end_date=data.end_date
        )
        return build_marriage_response(updated)

    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Database constraint violated")

@router.get("")
def get_marriage_list(db: Session = Depends(get_db)):
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

@router.get("/detail/{marriage_id}")
def get_marriage_detail(marriage_id: int, db: Session = Depends(get_db)):
    marriage = (
        db.query(Marriage)
        .options(
            joinedload(Marriage.spouse_a),
            joinedload(Marriage.spouse_b),
        )
        .filter(Marriage.id == marriage_id)
        .first()
    )

    if not marriage:
        raise HTTPException(status_code=404, detail="Marriage not found")

    return marriage_payload(marriage)

@router.get("/timeline/{person_id}")
def get_timeline(person_id: int, db: Session = Depends(get_db)):

    timeline = build_marriage_timeline(db, person_id)
# ⚠️ TODO (DAY 4):
# Current implementation = snapshot (NOT real timeline)
# Only returns final state of each marriage
# Need to refactor to event-based timeline:
# - married event (start_date)
# - status change event (end_date / status_changed_at)    
    return timeline

@router.get("/by-person/{person_id}", response_model=MarriageResponse)
def get_display(person_id: int, db: Session = Depends(get_db)):    
    
    marriages = get_display_marriage(db, person_id)

    if not marriages:
        raise HTTPException(status_code=404, detail="Không tìm thấy relationship")

    return build_marriage_response(marriages)
