from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date
from enum import Enum


# ==========================================================
# ENUM — Marriage Status
# ==========================================================
class MarriageStatus(str, Enum):
    married = "married"
    cohabiting = "cohabiting"
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
    priority: int = 0

    ceremony_type: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

    consanguineous: bool = False
    allow_underage: bool = False 
    
    @model_validator(mode="after")
    def validate_all(self):
        return self


# ==========================================================
# UPDATE
# ==========================================================
class MarriageUpdate(BaseModel):
    status: Optional[MarriageStatus] = None
    priority: Optional[int] = 0
    end_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_status(self):
        # if self.status == MarriageStatus.widowed:
        #     raise ValueError("Không được set status = widowed trực tiếp")

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

    status: Optional[str]
    computed_status: Optional[str]

    ceremony_type: Optional[str]
    location: Optional[str]
    notes: Optional[str]

    consanguineous: bool

    allow_underage: bool = False
class Config:
    from_attributes = True