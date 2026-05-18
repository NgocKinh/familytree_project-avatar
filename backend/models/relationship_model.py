from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.db import Base


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True, index=True)

    person_id_1 = Column(Integer, ForeignKey("persons.id"), nullable=False)
    person_id_2 = Column(Integer, ForeignKey("persons.id"), nullable=False)

    # Optional: loại quan hệ (father, mother, spouse...)
    relation_type = Column(Integer, nullable=True)

    # Relationships ORM (optional nhưng nên có)
    person1 = relationship("Person", foreign_keys=[person_id_1])
    person2 = relationship("Person", foreign_keys=[person_id_2])

    __table_args__ = (
        # ❌ Không cho self relationship
        CheckConstraint(
            "person_id_1 <> person_id_2",
            name="chk_no_self_relationship"
        ),

        # ✅ Chuẩn hóa direction: luôn person_id_1 < person_id_2
        CheckConstraint(
            "person_id_1 < person_id_2",
            name="chk_ordered_pair"
        ),

        # ✅ Không cho duplicate (A,B) trùng nhau
        UniqueConstraint(
            "person_id_1",
            "person_id_2",
            name="uq_relationship_pair"
        ),
    )