from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, case, desc, func
from datetime import datetime

from backend.models import Person, Marriage
from backend.constants.marriage_constants import ACTIVE_MARRIAGE_STATUSES
from backend.models.marriage_model import MarriageStatus, EndedByEnum
from backend.schemas.marriage_schema import MarriageCreate
from backend.core.exceptions import BadRequestException, AppError
from backend.domain.policies.policy_factory import create_marriage_policy

# ==========================================================
# HELPER
# ==========================================================

def normalize_person_ids(a: int, b: int):
    if a == b:
        raise AppError(
            error="SELF_RELATIONSHIP",
            message="Self relationship is not allowed",
            details={"person1_id": a, "person2_id": b}
        )
    return (min(a, b), max(a, b))


def get_partner(m: Marriage, person_id: int):
    if m.spouse_a_id == person_id:
        return m.spouse_b
    elif m.spouse_b_id == person_id:
        return m.spouse_a
    return None


def get_computed_status(m: Marriage):
    if m.status == MarriageStatus.widowed:
        return "widowed"
    return m.status.value if m.status else None

# ==========================================================
# CREATE
# ==========================================================

def create_marriage(db: Session, data: MarriageCreate):
    policy = create_marriage_policy()
    
    # ===== DEBUG END =====
    # normalize upfront
    spouse_a_id, spouse_b_id = (
        data.spouse_a_id,
        data.spouse_b_id
    )

    # self-marriage check
    if spouse_a_id == spouse_b_id:
        raise AppError(
            error="SELF_RELATIONSHIP",
            message="Self relationship is not allowed",
            details={"person1_id": spouse_a_id, "person2_id": spouse_b_id}
        )

    # check person tồn tại
    person_a = db.get(Person, spouse_a_id)
    person_b = db.get(Person, spouse_b_id)
    if not person_a or not person_b:
        raise BadRequestException("Person not found")

    # check existing
    existing = db.query(Marriage).filter(
        Marriage.status.in_(ACTIVE_MARRIAGE_STATUSES),
        or_(
            # (a,b)
            (Marriage.spouse_a_id == spouse_a_id) &
            (Marriage.spouse_b_id == spouse_b_id),

            # (b,a)
            (Marriage.spouse_a_id == spouse_b_id) &
            (Marriage.spouse_b_id == spouse_a_id),
        )
    ).with_for_update().all()

    policy.validate_marriage(person_a, person_b, existing)

    # create marriage
    marriage = Marriage(
        spouse_a_id=spouse_a_id,
        spouse_b_id=spouse_b_id,
        start_date=data.start_date,
        end_date=data.end_date,
        status=data.status,
        priority=data.priority,
    )

    db.add(marriage)
    db.commit()
    db.refresh(marriage)

    return marriage

def end_marriage(db: Session, marriage_id: int, reason: str, end_date):
    policy = create_marriage_policy()
    # ❗ NORMALIZE & VALIDATE REASON
    if not reason:
        raise BadRequestException("Status is required")

    # clean input mạnh hơn
    reason = reason.strip().lower().replace('"', '').replace("'", "")

    if reason == "":
        raise BadRequestException("Status is required")

    if reason not in ["divorced", "death"]:
        raise BadRequestException("Invalid end reason")

    marriage = db.query(Marriage).filter(
        Marriage.id == marriage_id
    ).execution_options(populate_existing=True).first()

    if not marriage:
        raise BadRequestException("Marriage not found")
    # ❗ VALIDATE END DATE
    if end_date and marriage.start_date and end_date < marriage.start_date:
        raise BadRequestException("end_date cannot be before start_date")
    
    # ✅ SINGLE SOURCE OF TRUTH
    policy.validate_end_marriage(marriage, reason)

    # ✅ update only
    marriage.end_date = end_date
    from backend.models.marriage_model import EndedByEnum
    marriage.ended_by = EndedByEnum(reason)

    if reason == "divorced":
        marriage.status = MarriageStatus.divorced
    elif reason == "death":
        marriage.status = MarriageStatus.widowed

    marriage.status_changed_at = datetime.utcnow()

    db.commit()
    db.refresh(marriage)

    return marriage
# ==========================================================
# GET SPOUSES
# ==========================================================

def get_active_marriages(db: Session, person_id: int):

    return db.query(Marriage).filter(
        or_(
            Marriage.spouse_a_id == person_id,
            Marriage.spouse_b_id == person_id
        ),
        Marriage.status.in_(ACTIVE_MARRIAGE_STATUSES)
    ).all()

def get_spouses(db: Session, person_id: int):

    marriages = get_active_marriages(db, person_id)

    spouses = []
    seen_ids = set()

    for m in marriages:
        partner = get_partner(m, person_id)

        if partner and partner.id not in seen_ids:
            spouses.append(partner)
            seen_ids.add(partner.id)

    return spouses    

# ==========================================================
# DISPLAY & QUERY LOGIC
# ==========================================================

def get_display_marriage(db: Session, person_id: int):

    priority = case(
        (Marriage.status == MarriageStatus.married, 1),
        (Marriage.status == MarriageStatus.cohabiting, 2),
        (Marriage.status == MarriageStatus.divorced, 3),
        (Marriage.status == MarriageStatus.widowed, 4),
        else_=99
    )
    effective_date = func.coalesce(
        Marriage.status_changed_at,
        Marriage.start_date,
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
            desc(effective_date),
            priority.asc(),
            desc(Marriage.created_at)
        )
        .first()
    )

    return marriage

def get_all_marriages(db: Session, person_id: int = None):

    query = db.query(Marriage).options(
        joinedload(Marriage.spouse_a),
        joinedload(Marriage.spouse_b)
    )

    if person_id:
        return query.filter(
            or_(
                Marriage.spouse_a_id == person_id,
                Marriage.spouse_b_id == person_id
            )
        ).all()

    return query.all()

    return result

def get_marriage_by_id(db: Session, marriage_id: int):
    marriage = db.query(Marriage)\
        .options(
            joinedload(Marriage.spouse_a),
            joinedload(Marriage.spouse_b)
        )\
        .filter(Marriage.id == marriage_id)\
        .first()

    if not marriage:
        raise BadRequestException("Marriage not found")

    return marriage

def get_marriage_timeline(db: Session, person_id: int):

    marriages = get_all_marriages(db, person_id)

    def get_time(m):
        return (
            m.status_changed_at
            or m.start_date
            or m.created_at
        )

    marriages.sort(
        key=get_time,
        reverse=True
    )

    return marriages

def build_marriage_timeline(db: Session, person_id: int):
    # ⚠️ TODO (DAY 4):
    # This is NOT a real timeline (snapshot only)
    # Currently returns final state of marriages
    # Need refactor to event-based timeline:
    # - married event (start_date)
    # - status change event (end_date / status_changed_at)
    marriages = get_marriage_timeline(db, person_id)

    result = []

    for m in marriages:
        partner = get_partner(m, person_id)

        result.append({
            "marriage_id": m.id,
            "spouse_id": partner.id if partner else None,
            "status": m.status.value if m.status else None,
            "start_date": m.start_date,
            "end_date": m.end_date,
            "status_changed_at": m.status_changed_at
        })

    return result

    
# ==========================================================
# RESPONSE BUILDER
# ==========================================================

def get_full_name(p):
    if not p:
        return None

    parts = [
        p.sur_name,
        p.last_name,
        p.middle_name,
        p.first_name
    ]

    # lọc None + chuỗi rỗng
    parts = [x for x in parts if x and str(x).strip()]

    if not parts:
        return f"ID:{p.person_id}"  # fallback an toàn

    return " ".join(parts)


def build_marriage_response(m):
    if not m:
        return None

    return {
        "id": m.id,

        "spouse_a_id": m.spouse_a_id,
        "spouse_b_id": m.spouse_b_id,

        "spouse_a_name": get_full_name(m.spouse_a),
        "spouse_b_name": get_full_name(m.spouse_b),

        "start_date": m.start_date,
        "end_date": m.end_date,

        "status": m.status.value if m.status else None,
        "computed_status": get_computed_status(m),

        "ceremony_type": m.ceremony_type,
        "location": m.location,
        "notes": m.notes,

        "consanguineous": m.consanguineous,
    }
    
# ==========================================================
# DEATH TRIGGER
# ==========================================================

def handle_person_death(db: Session, person_id: int, death_date):
    marriages = db.query(Marriage).filter(
        or_(
            Marriage.spouse_a_id == person_id,
            Marriage.spouse_b_id == person_id
        )
    ).all()

    for m in marriages: # TODO: move this logic to domain service / event handler
        if m.status in ACTIVE_MARRIAGE_STATUSES: # TODO:
            m.ended_by = EndedByEnum.death
            m.end_date = death_date
            m.status = MarriageStatus.widowed
            m.status_changed_at = datetime.utcnow()

    db.commit()
    return marriages