from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.db import Base


class ParentChild(Base):
    __tablename__ = "parent_child"

    id = Column(Integer, primary_key=True, index=True)

    parent_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)
    child_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)

    type = Column(String, nullable=False)  # FATHER / MOTHER
    notes = Column(String, nullable=True)

    # 🔁 Relationship
    parent = relationship(
        "Person",
        foreign_keys=[parent_id],
        backref="children_relations"
    )

    child = relationship(
        "Person",
        foreign_keys=[child_id],
        backref="parent_relations"
    )