from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.db import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class ParentChild(Base):
    __tablename__ = "parent_child"

    id = Column(Integer, primary_key=True, index=True)

    parent_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)
    child_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)

    marriage_id = Column(Integer, nullable=True)
    type = Column(String(10), nullable=False)
    notes = Column(Text, nullable=True)

    parent = relationship(
        "Person",
        foreign_keys=[parent_id],
        backref="children_relations"
    )
    # 🔵 [ADDED]: relationship child
    child = relationship(
        "Person",
        foreign_keys=[child_id],
        backref="parent_relations"
    )
    __table_args__ = (
        UniqueConstraint("parent_id", "child_id", "type", name="uq_parent_child"),
    )