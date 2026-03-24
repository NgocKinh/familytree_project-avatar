from sqlalchemy.orm import Session
from sqlalchemy import or_, case, desc, func
from datetime import datetime

from backend.models.marriage_model import Marriage
from backend.schemas.marriage import MarriageCreate


# ==========================================================
# HELPER
# ==========================================================

def normalize_person_ids(a: int, b: int):
    return (min(a, b), max(a, b))


def get_partner(m: Marriage, person_id: int):
    if m.spouse_a_id == person_id:
        return m.spouse_b
    return m.spouse_a


def get_computed_status(m: Marriage):
    if m.ended_by == "death":
        return "widowed"
    return m.status


# ==========================================================
# EXISTING FUNCTION (GIỮ NGUYÊN + CLEAN NHẸ)
# ==========================================================

def get_spouses(db: Session, person_id: int):
    marriages = db.query(Marriage).filter(
        or_(
            Marriage.spouse_a_id == person_id,
            Marriage.spouse_b_id == person_id
        )
    ).all()

    spouses = []

    for m in marriages:
        partner = get_partner(m, person_id)
        spouses.append(partner)

    return spouses


# ==========================================================
# CREATE
# ==========================================================

def create_marriage(db: Session, data: MarriageCreate):
    p1, p2 = normalize_person_ids(
        data.spouse_a_id,
        data.spouse_b_id
    )

    marriage = Marriage(
        spouse_a_id=p1,
        spouse_b_id=p2,

        status=data.status.value,

        start_date=data.start_date,
        end_date=data.end_date,

        ceremony_type=data.ceremony_type,
        location=data.location,
        notes=data.notes,

        consanguineous=data.consanguineous,

        created_at=datetime.utcnow(),
        status_changed_at=datetime.utcnow()
    )

    db.add(marriage)
    db.commit()
    db.refresh(marriage)

    return marriage


# ==========================================================
# DISPLAY LOGIC (CORE)
# ==========================================================

def get_display_marriage(db: Session, person_id: int):
    """
    Trả về 1 marriage đại diện để hiển thị tree
    """

    from sqlalchemy import case

    priority = case(
        (Marriage.status == "married", 1),
        (Marriage.status == "cohabiting", 2),
        (Marriage.status == "divorced", 3),
        (Marriage.status == "widowed", 4),
        else_=99
    )

    effective_date = func.coalesce(
        Marriage.start_date,
        Marriage.status_changed_at,
        Marriage.created_at
    )

    marriage = (
        db.query(Marriage)
        .filter(
            or_(
                Marriage.spouse_a_id == person_id,
                Marriage.spouse_b_id == person_id
            )
        )
        .order_by(
            Marriage.ended_by.is_(None),      # active trước
            priority.asc(),                   # ưu tiên loại quan hệ
            desc(effective_date),             # timeline
            desc(Marriage.created_at)         # fallback
        )
        .first()
    )

    return marriage


# ==========================================================
# RESPONSE BUILDER
# ==========================================================

def build_marriage_response(m: Marriage):
    if not m:
        return None

    return {
        "id": m.id,
        "spouse_a_id": m.spouse_a_id,
        "spouse_b_id": m.spouse_b_id,

        "start_date": m.start_date,
        "end_date": m.end_date,

        "status": m.status,
        "computed_status": get_computed_status(m),

        "ceremony_type": m.ceremony_type,
        "location": m.location,
        "notes": m.notes,

        "consanguineous": m.consanguineous
    }


# ==========================================================
# DEATH TRIGGER (CHƯA GỌI NGAY - DÙNG SAU)
# ==========================================================

def handle_person_death(db: Session, person_id: int, death_date):
    marriages = db.query(Marriage).filter(
        or_(
            Marriage.spouse_a_id == person_id,
            Marriage.spouse_b_id == person_id
        )
    ).all()

    for m in marriages:
        if m.ended_by is None:
            m.ended_by = "death"
            m.end_date = death_date
            m.status_changed_at = datetime.utcnow()

    db.commit()