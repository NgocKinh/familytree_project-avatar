# File: backend/services/marriage_service.py

from sqlalchemy.orm import Session
from backend.models.marriage_model import Marriage


def get_spouses(db: Session, person_id: int):
    marriages = db.query(Marriage).filter(
        (Marriage.spouse_a_id == person_id) |
        (Marriage.spouse_b_id == person_id)
    ).all()

    spouses = []

    for m in marriages:
        if m.spouse_a_id == person_id:
            spouses.append(m.spouse_b)
        else:
            spouses.append(m.spouse_a)

    return spouses