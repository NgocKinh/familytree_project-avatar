from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    role: str = "viewer"
    person_id: Optional[int] = None
    is_active: bool = True


class UserUpdate(BaseModel):
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    person_id: Optional[int] = None
    is_active: Optional[bool] = None