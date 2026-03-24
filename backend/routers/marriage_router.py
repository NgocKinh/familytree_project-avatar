from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.db import get_db
from backend.schemas.marriage import MarriageCreate, MarriageResponse
from backend.services.marriage_service import (
    create_marriage,
    get_display_marriage,
    build_marriage_response
)

router = APIRouter(prefix="/marriage", tags=["Marriage"])


# ==========================================================
# CREATE MARRIAGE
# ==========================================================
@router.post("/", response_model=MarriageResponse)
def create(data: MarriageCreate, db: Session = Depends(get_db)):
    marriage = create_marriage(db, data)
    return build_marriage_response(marriage)


# ==========================================================
# GET DISPLAY MARRIAGE (MULTIPLE RELATIONSHIPS - POLYGAMY)
# ==========================================================
@router.get("/{person_id}", response_model=List[MarriageResponse])
def get_display(person_id: int, db: Session = Depends(get_db)):
    marriages = get_display_marriage(db, person_id)

    if not marriages:
        raise HTTPException(status_code=404, detail="Không tìm thấy relationship")

    return [build_marriage_response(m) for m in marriages]