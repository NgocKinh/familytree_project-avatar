from sqlalchemy.orm import Session
from backend.models.person_model import Person
from backend.schemas.person_schema import PersonCreate, PersonUpdate
from backend.core.exceptions import NotFoundException


def get_person_or_404(db: Session, person_id: int) -> Person:
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.delete_status == 0
    ).first()

    if not person:
        raise NotFoundException("Person not found")

    return person


def create_person(db: Session, payload: PersonCreate) -> Person:
    person = Person(**payload.dict())

    db.add(person)
    db.commit()
    db.refresh(person)

    return person


def update_person(db: Session, person_id: int, payload: PersonUpdate) -> Person:
    person = get_person_or_404(db, person_id)

    for k, v in payload.items():
        setattr(person, k, v)

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