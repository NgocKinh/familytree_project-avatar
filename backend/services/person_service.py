from sqlalchemy.orm import Session
from backend.models.person_model import Person
from backend.schemas.person_schema import PersonCreate, PersonUpdate
from backend.core.exceptions import NotFoundException
from backend.services.audit_log_service import write_audit_log

def get_person_or_404(db: Session, person_id: int) -> Person:
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.delete_status == 0
    ).first()

    if not person:
        raise NotFoundException("Person not found")

    return person


def create_person(
    db: Session,
    payload: PersonCreate,
    current_user,
) -> Person:
    person = Person(**payload.dict())

    db.add(person)
    db.flush()

    write_audit_log(
        db=db,
        current_user=current_user,
        action="CREATE",
        entity_type="person",
        entity_id=person.id,
        description=f"Tạo thành viên mới ID {person.id}",
    )

    db.commit()
    db.refresh(person)

    return person

def update_person(
    db: Session,
    person_id: int,
    payload: PersonUpdate,
    current_user,
) -> Person:
    person = get_person_or_404(db, person_id)

    payload.pop("created_at", None)
    payload.pop("updated_at", None)
    payload.pop("avatar", None)

    for k, v in payload.items():
        setattr(person, k, v)

    write_audit_log(
        db=db,
        current_user=current_user,
        action="UPDATE",
        entity_type="person",
        entity_id=person_id,
        description=f"Cập nhật thông tin thành viên ID {person_id}",
    )

    db.commit()
    db.refresh(person)

    return person

def delete_person(db: Session, person_id: int):
    person = get_person_or_404(db, person_id)

    db.query(Person).filter(Person.id == person_id).update({
        "delete_status": 1
    })

    db.commit()

def get_person(db: Session, person_id: int) -> Person:
    return get_person_or_404(db, person_id)


from sqlalchemy import asc, desc

def get_all_persons(db: Session):
    # ✅ [CHANGE 1]: Lấy cả người hoạt động và đã ẩn để frontend tự chia tab
    return db.query(Person).order_by(
        Person.birth_date.is_(None),
        desc(Person.birth_date),
        asc(Person.first_name)
    ).all()