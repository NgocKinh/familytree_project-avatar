from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Enum, Text, JSON
)
from sqlalchemy.orm import relationship
from backend.db import Base
from datetime import datetime
import enum

# 🔹 Enum (match DB)
class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    other = "other"


class DatePrecisionEnum(str, enum.Enum):
    unknown = "unknown"
    year = "year"
    month = "month"
    exact = "exact"


class AsianDatePrecisionEnum(str, enum.Enum):
    exact = "exact"
    month = "month"
    year = "year"
    unknown = "unknown"


class MarriageRoleEnum(str, enum.Enum):
    husband = "husband"
    wife = "wife"
    unknown = "unknown"


class Person(Base):
    __tablename__ = "persons"

    # 🔑 PK
    id = Column("person_id", Integer, primary_key=True)

    lineage_id = Column(Integer, nullable=True)

    # 🧾 Name
    sur_name = Column(String(150), nullable=True)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=False)
    full_name_vn = Column(String(350), nullable=True)
    # 🔵 [ADDED]: full name chuẩn, không phụ thuộc cột full_name_vn
    @property
    def full_name(self):
        return " ".join(
            str(part).strip()
            for part in [
                self.sur_name,
                self.last_name,
                self.middle_name,
                self.first_name,
            ]
            if part and str(part).strip()
        )
    # 👤 Basic
    gender = Column(Enum(GenderEnum), nullable=False, default=GenderEnum.other)

    birth_date = Column(Date, nullable=True)
    birth_date_precision = Column(
        Enum(DatePrecisionEnum), nullable=True, default=DatePrecisionEnum.unknown
    )
    birth_order = Column(Integer, nullable=True)
    
    death_date = Column(Date, nullable=True)
    death_date_precision = Column(
        Enum(DatePrecisionEnum), nullable=True, default=DatePrecisionEnum.unknown
    )

    # 🏮 Asian date
    asian_birth_date = Column(Text, nullable=True)
    asian_birth_precision = Column(
        Enum(AsianDatePrecisionEnum), nullable=False, default=AsianDatePrecisionEnum.unknown
    )

    asian_death_date = Column(Text, nullable=True)
    asian_death_precision = Column(
        Enum(AsianDatePrecisionEnum), nullable=False, default=AsianDatePrecisionEnum.unknown
    )

    # 📍 Location
    birth_place = Column(String(200), nullable=True)
    death_place = Column(String(200), nullable=True)
    grave_info = Column(String(255), nullable=True)

    anniversary_death = Column(String(10), nullable=True)
    anniversary_type = Column(String(20), nullable=True)
    # 🌍 Info
    nationality = Column(String(100), nullable=True)
    ethnic_group = Column(String(100), nullable=True)
    religion = Column(String(200), nullable=True)

    languages_spoken = Column(JSON, nullable=True)

    # 📞 Contact
    address = Column(String(255), nullable=True)
    phone_number = Column(String(32), nullable=True)
    email = Column(String(255), nullable=True)

    # 🖼️ Media
    avatar = Column(String(255), nullable=True)

    # 🎓 Education
    school_attended = Column(String(255), nullable=True)
    degree_earned = Column(String(255), nullable=True)

    # 🕒 Meta
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    delete_status = Column(Integer, default=0)

    notes = Column(Text, nullable=True)

    # 🧬 Extra
    blood_code = Column(String(20), nullable=True)

    role_in_marriage = Column(
        Enum(MarriageRoleEnum), nullable=True, default=MarriageRoleEnum.unknown
    )

    # 💍 Marriage
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

    @property
    def marriages(self):
        return self.marriages_as_a + self.marriages_as_b