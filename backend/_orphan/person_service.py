
from sqlalchemy.orm import Session
from backend.models.person_model import Person


def get_person_gender(db: Session, person_id: int) -> str | None:
    person = db.query(Person).filter(
        Person.id == person_id,
        Person.delete_status == 0
    ).first()

    return person.gender if person else None