from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# 🔹 Enum (match model)
class GenderEnum(str):
    male = "male"
    female = "female"
    other = "other"


class DatePrecisionEnum(str):
    unknown = "unknown"
    year = "year"
    month = "month"
    exact = "exact"


class AsianDatePrecisionEnum(str):
    exact = "exact"
    month = "month"
    year = "year"
    unknown = "unknown"


class MarriageRoleEnum(str):
    husband = "husband"
    wife = "wife"
    unknown = "unknown"


# 🔹 Marriage (rút gọn tránh loop)
class MarriageBase(BaseModel):
    id: int
    spouse_a_id: int
    spouse_b_id: int
    status: str

    class Config:
        from_attributes = True


# 🔹 Person base (FULL theo DB)
class PersonBase(BaseModel):
    lineage_id: Optional[int] = None

    # Name
    sur_name: Optional[str] = None
    last_name: str
    middle_name: Optional[str] = None
    first_name: str

    # Basic
    gender: Optional[str] = None

    birth_date: Optional[date] = None
    birth_date_precision: Optional[str] = None

    death_date: Optional[date] = None
    death_date_precision: Optional[str] = None

    # Asian date
    asian_birth_date: Optional[str] = None
    asian_birth_precision: Optional[str] = None

    asian_death_date: Optional[str] = None
    asian_death_precision: Optional[str] = None

    # Location
    birth_place: Optional[str] = None
    death_place: Optional[str] = None
    grave_info: Optional[str] = None

    anniversary_death: Optional[str] = None

    # Info
    nationality: Optional[str] = None
    ethnic_group: Optional[str] = None
    religion: Optional[str] = None

    languages_spoken: Optional[List[str]] = None

    # Contact
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

    # Media
    avatar: Optional[str] = None

    # Education
    school_attended: Optional[str] = None
    degree_earned: Optional[str] = None

    # Meta
    deleted_at: Optional[datetime] = None
    delete_status: Optional[int] = None

    notes: Optional[str] = None

    # Extra
    blood_code: Optional[str] = None
    role_in_marriage: Optional[str] = None


# 🔹 Create
class PersonCreate(PersonBase):
    pass


# 🔹 Update
class PersonUpdate(PersonBase):
    pass


# 🔹 Response (có marriages)
class PersonResponse(PersonBase):
    id: int

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    marriages: List[MarriageBase] = []

    class Config:
        from_attributes = True
# ==========================================================
# RESPONSE - BASIC ⭐ (ADD NEW)
# ==========================================================
class PersonBasicResponse(BaseModel):
    id: int

    sur_name: Optional[str]
    last_name: str
    middle_name: Optional[str]
    first_name: str

    gender: Optional[str]

    birth_date: Optional[date]
    death_date: Optional[date]

    avatar: Optional[str]

    class Config:
        from_attributes = True


# ==========================================================
# RESPONSE - DETAIL ⭐ (ADD NEW)
# ==========================================================
class PersonDetailResponse(BaseModel):
    id: int

    # Name
    sur_name: Optional[str]
    last_name: str
    middle_name: Optional[str]
    first_name: str

    # Basic
    gender: Optional[str]
    birth_date: Optional[date]
    birth_date_precision: Optional[str]

    death_date: Optional[date]
    death_date_precision: Optional[str]

    # Asian
    asian_birth_date: Optional[str]
    asian_birth_precision: Optional[str]

    asian_death_date: Optional[str]
    asian_death_precision: Optional[str]

    # Location
    birth_place: Optional[str]
    death_place: Optional[str]
    grave_info: Optional[str]

    # Info
    nationality: Optional[str]
    ethnic_group: Optional[str]
    religion: Optional[str]

    # Contact
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]

    # Media
    avatar: Optional[str]

    # Education
    school_attended: Optional[str]
    degree_earned: Optional[str]

    # Extra
    blood_code: Optional[str]
    role_in_marriage: Optional[str]

    notes: Optional[str]

    class Config:
        from_attributes = True