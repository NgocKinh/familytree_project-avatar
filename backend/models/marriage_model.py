# File: backend/models/marriage_model.py

from sqlalchemy import Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.db import Base


class Marriage(Base):
    __tablename__ = "marriages"

    id = Column(Integer, primary_key=True, index=True)

    spouse_a = relationship(
        "Person",
        foreign_keys=[spouse_a_id],
        back_populates="marriages_as_a"
    )

    spouse_b = relationship(
        "Person",
        foreign_keys=[spouse_b_id],
        back_populates="marriages_as_b"
    )

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    status = Column(String, nullable=True)
    ceremony_type = Column(String, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    consanguineous = Column(Integer, default=0)

    spouse_a = relationship("Person", foreign_keys=[spouse_a_id])
    spouse_b = relationship("Person", foreign_keys=[spouse_b_id])