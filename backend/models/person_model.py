# File: backend/models/person_model.py

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from backend.db import Base


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    gender = Column(String, nullable=True)

    birth_date = Column(Date, nullable=True)
    death_date = Column(Date, nullable=True)

    father_id = Column(Integer, nullable=True)
    mother_id = Column(Integer, nullable=True)

    notes = Column(String, nullable=True)

    marriages_as_a = relationship(
    "Marriage",
    foreign_keys="Marriage.spouse_a_id",
    back_populates="spouse_a"
)

marriages_as_b = relationship(
    "Marriage",
    foreign_keys="Marriage.spouse_b_id",
    back_populates="spouse_b"
)