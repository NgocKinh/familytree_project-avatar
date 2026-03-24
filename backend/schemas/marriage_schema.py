from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date
from enum import Enum


# ==========================================================
# ENUM — Marriage Status
# ==========================================================
class MarriageStatus(str, Enum):
    married = "married"
    cohabitation = "cohabitation"
    separated = "separated"
    divorced = "divorced"
    widowed = "widowed"


# ==========================================================
# CREATE
# ==========================================================
class MarriageCreate(BaseModel):
    spouse_a_id: int = Field(..., example=1)
    spouse_b_id: int = Field(..., example=2)

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    # ✅ FIX: không nên optional
    status: MarriageStatus = MarriageStatus.married

    ceremony_type: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    consanguineous: bool = False

    @model_validator(mode="after")
    def validate_all(self):
        # ❌ Không cho cưới chính mình
        if self.spouse_a_id == self.spouse_b_id:
            raise ValueError("Hai spouse không được trùng nhau")

        # ❌ Không cho set widowed bằng tay
        if self.status == MarriageStatus.widowed:
            raise ValueError("Không được set status = widowed trực tiếp")

        # ⚠️ OPTIONAL: validate timeline
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date phải >= start_date")

        return self


# ==========================================================
# UPDATE
# ==========================================================
class MarriageUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    status: Optional[MarriageStatus] = None
    ceremony_type: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    consanguineous: Optional[bool] = None

    @model_validator(mode="after")
    def validate_status(self):
        if self.status == MarriageStatus.widowed:
            raise ValueError("Không được set status = widowed trực tiếp")

        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValueError("end_date phải >= start_date")

        return self


# ==========================================================
# RESPONSE (OPTIONAL — dùng cho GET)
# ==========================================================
class MarriageResponse(BaseModel):
    id: int  # ✅ rename cho thống nhất

    spouse_a_id: int
    spouse_b_id: int

    start_date: Optional[date]
    end_date: Optional[date]

    status: Optional[MarriageStatus]  # status gốc DB

    ceremony_type: Optional[str]
    location: Optional[str]
    notes: Optional[str]

    consanguineous: bool

class Config:
    from_attributes = True