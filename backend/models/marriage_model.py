from sqlalchemy import Column, Integer, Date, String, ForeignKey, DateTime, Enum, Text, Boolean, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.db import Base
from datetime import datetime
import enum
from .person_model import Person
def normalize_spouses(a_id: int, b_id: int):
    return (a_id, b_id) if a_id < b_id else (b_id, a_id)

# 🔹 Enum chuẩn (giữ từ code bạn)
class MarriageStatus(str, enum.Enum):
    married = "married"
    cohabiting = "cohabiting"
    separated = "separated"
    divorced = "divorced"
    widowed = "widowed"

ACTIVE_MARRIAGE_STATUSES = [
    MarriageStatus.married,
    MarriageStatus.cohabiting,
]

class CeremonyTypeEnum(str, enum.Enum):
    civil = "civil"
    religious = "religious"
    customary = "customary"

class EndedByEnum(str, enum.Enum):
    divorced = "divorced"
    death = "death"
    annulment = "annulment"

class Marriage(Base):
    __tablename__ = "marriages"
    # ⚠️ remove unique constraint cũ → sẽ thay bằng partial index ở migration
    __table_args__ = (
        CheckConstraint("spouse_a_id != spouse_b_id", name="check_not_self_marriage"),
        CheckConstraint(
            """
            (status IN ('divorced', 'widowed') AND end_date IS NOT NULL)
            OR
            (status IN ('married', 'cohabiting', 'separated') AND end_date IS NULL)
            """,
            name="check_status_end_date_consistency"
        ),      
    )
    # 🔑 Primary key
    id = Column(Integer, primary_key=True)

    # 🔗 Foreign keys → persons.person_id
    spouse_a_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)
    spouse_b_id = Column(Integer, ForeignKey("persons.person_id"), nullable=False)

    # 🔁 Relationship 2 chiều (GIỮ từ code bạn → rất chuẩn)
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

    # 📊 Status (giữ enum bạn + chuẩn hoá)
    status = Column(
        Enum(MarriageStatus),
        nullable=False,
        default=MarriageStatus.married
    )

    # ⭐ Ưu tiên hiển thị hôn nhân trên Tree
    priority = Column(Integer, default=0)

    # 🧠 Logic kết thúc
    ended_by = Column(Enum(EndedByEnum), nullable=True)
    status_changed_at = Column(DateTime, nullable=True)

    # 📍 Metadata (NÂNG CẤP)
    ceremony_type = Column(Enum(CeremonyTypeEnum), nullable=True)   # ✅ tốt hơn String
    location = Column(String(200), nullable=True)                   # ✅ fix length
    notes = Column(Text, nullable=True)                             # ✅ Text thay vì String
    
    # 🧬 Quan hệ huyết thống gần
    consanguineous = Column(Boolean, default=False)

    # 🕒 Thời điểm tạo
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)