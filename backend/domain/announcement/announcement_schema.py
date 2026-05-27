from pydantic import BaseModel
from typing import Optional


# ======================================================
# CREATE ANNOUNCEMENT
# ======================================================

class AnnouncementCreate(BaseModel):

    title: str
    description: Optional[str] = None

    event_type: str
    calendar_type: str

    solar_date: Optional[str] = None

    lunar_day: Optional[int] = None
    lunar_month: Optional[int] = None
    lunar_year: Optional[int] = None

    repeat_type: str = "yearly"

    person_id: Optional[int] = None

    is_active: bool = True


# ======================================================
# RESPONSE MODEL
# ======================================================

class AnnouncementResponse(BaseModel):

    id: int

    title: str
    description: Optional[str] = None

    event_type: str
    calendar_type: str

    solar_date: Optional[str] = None

    lunar_day: Optional[int] = None
    lunar_month: Optional[int] = None
    lunar_year: Optional[int] = None

    repeat_type: str

    person_id: Optional[int] = None

    is_active: bool

    class Config:
        from_attributes = True