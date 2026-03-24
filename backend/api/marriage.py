# ==========================================================
# File: backend/api/marriage.py (REFactored - ORM ONLY)
# ==========================================================

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

# ==========================================================
# DATABASE
# ==========================================================
from backend.db import get_db

# ==========================================================
# MODELS
# ==========================================================
from backend.models.marriage_model import Marriage
from backend.models.person_model import Person

# ==========================================================
# SCHEMAS
# ==========================================================
from backend.schemas.marriage_schema import (
    MarriageCreate,
    MarriageUpdate,
    MarriageResponse
)
router = APIRouter()
# ==========================================================
# CREATE MARRIAGE
# ==========================================================
@router.post("/marriage", status_code=status.HTTP_201_CREATED)
def create_marriage_api(
    data: MarriageCreate,
    db: Session = Depends(get_db)
):

    # ❗ Check persons exist
    persons = db.query(Person).filter(
        Person.id.in_([data.spouse_a_id, data.spouse_b_id])
    ).all()

    if len(persons) != 2:
        raise HTTPException(404, "One or both persons not found")

    # ❗ Check duplicate marriage (A-B or B-A)
    exists = db.query(Marriage).filter(
        or_(
            (Marriage.spouse_a_id == data.spouse_a_id) &
            (Marriage.spouse_b_id == data.spouse_b_id),
            (Marriage.spouse_a_id == data.spouse_b_id) &
            (Marriage.spouse_b_id == data.spouse_a_id)
        )
    ).first()

    if exists:
        raise HTTPException(409, "Marriage already exists")

    marriage = Marriage(**data.dict())

    db.add(marriage)
    db.commit()
    db.refresh(marriage)

    return marriage


# ==========================================================
# GET ALL MARRIAGES
# ==========================================================
@router.get("/marriage", response_model=list[MarriageResponse])
def get_all_marriages(db: Session = Depends(get_db)):
    return db.query(Marriage).all()


# ==========================================================
# GET ONE MARRIAGE
# ==========================================================
@router.get("/marriage/{mid}", response_model=MarriageResponse)
def get_marriage(mid: int, db: Session = Depends(get_db)):
    marriage = db.query(Marriage).filter(Marriage.id == mid).first()

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    return marriage


# ==========================================================
# UPDATE MARRIAGE
# ==========================================================
@router.put("/marriage/{mid}")
def update_marriage(mid: int, data: MarriageUpdate, db: Session = Depends(get_db)):
    marriage = db.query(Marriage).filter(Marriage.id == mid).first()

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(marriage, key, value)

    db.commit()
    db.refresh(marriage)

    return marriage


# ==========================================================
# DELETE MARRIAGE
# ==========================================================
@router.delete("/marriage/{mid}")
def delete_marriage(mid: int, db: Session = Depends(get_db)):
    marriage = db.query(Marriage).filter(Marriage.id == mid).first()

    if not marriage:
        raise HTTPException(404, "Marriage not found")

    db.delete(marriage)
    db.commit()

    return {"message": "Deleted successfully"}


# ==========================================================
# GET ALL MARRIAGES OF A PERSON (HISTORY)
# ==========================================================
@router.get("/marriage/person/{person_id}", response_model=list[MarriageResponse])
def get_person_marriages(person_id: int, db: Session = Depends(get_db)):
    marriages = db.query(Marriage).filter(
        or_(
            Marriage.spouse_a_id == person_id,
            Marriage.spouse_b_id == person_id
        )
    ).all()

    return marriages
