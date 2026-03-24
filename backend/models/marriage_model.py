from sqlalchemy import Column, Integer, Date, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from backend.db import Base
from datetime import datetime
import enum


# ✅ Enum chuẩn (đã có cohabitation)
class MarriageStatus(str, enum.Enum):
    married = "married"
    cohabitation = "cohabitation"
    separated = "separated"
    divorced = "divorced"
    widowed = "widowed"


class Marriage(Base):
    __tablename__ = "marriages"

    # 🔑 Primary key
    id = Column(Integer, primary_key=True, index=True)

    # 🔗 Foreign keys → persons.person_id
    spouse_a_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)
    spouse_b_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)

    # 🔁 Relationship 2 chiều với Person
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

    # 📅 Timeline
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    # 📊 Status (Enum + default)
    status = Column(
        Enum(MarriageStatus),
        nullable=False,
        default=MarriageStatus.married
    )

    # 🧠 Logic kết thúc
    ended_by = Column(String, nullable=True)  # divorce / death
    status_changed_at = Column(DateTime, nullable=True)

    # 📍 Metadata
    ceremony_type = Column(String, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # 🧬 Quan hệ huyết thống gần
    consanguineous = Column(Integer, default=0)

    # 🕒 Thời điểm tạo
    created_at = Column(DateTime, default=datetime.utcnow)