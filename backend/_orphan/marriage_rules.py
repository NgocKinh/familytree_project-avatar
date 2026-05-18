
from backend.models.marriage_model import Marriage
from backend.core.exceptions import BadRequestException
from sqlalchemy import or_

# DEPRECATED — DO NOT USE

def validate_same_sex(person1, person2, policy):

    if policy.allow_same_sex():
        return

    if person1.gender == person2.gender:
        raise BadRequestException("Same-sex marriage is not allowed by configuration.")

def validate_multiple_spouses(db, person1_id, person2_id, policy):

    from backend.constants.marriage_constants import ACTIVE_MARRIAGE_STATUSES

    if policy.allow_multiple_spouses():
        return

# Validate active marriages
    active_marriages = (
        db.query(Marriage)
        .filter(
            or_(
                (Marriage.spouse_a_id == person1_id), 
                (Marriage.spouse_b_id == person1_id), 
                (Marriage.spouse_a_id == person2_id), 
                (Marriage.spouse_b_id == person2_id),
            ),
            Marriage.status.in_(ACTIVE_MARRIAGE_STATUSES)
        )
        .all()
    )

    if len(active_marriages) > 0:
        raise BadRequestException("Multiple spouses are not allowed.")

def validate_marriage_rules(db, person1, person2):
    from backend.domain.policies.policy_factory import get_marriage_policy
    policy = get_marriage_policy()
    close_existing_marriages(db, person1.id)
    close_existing_marriages(db, person2.id)
    validate_same_sex(person1, person2, policy)
    validate_multiple_spouses(db, person1.id, person2.id, policy)

def close_existing_marriages(db, person_id):
    from backend.constants.marriage_constants import ACTIVE_MARRIAGE_STATUSES

    existing = db.query(Marriage).filter(
        or_(
            (Marriage.spouse_a_id == person_id),
            (Marriage.spouse_b_id == person_id),
        ),
        Marriage.status.in_(ACTIVE_MARRIAGE_STATUSES)
    ).all()

    for m in existing:
        m.status = "divorced"
    db.flush()