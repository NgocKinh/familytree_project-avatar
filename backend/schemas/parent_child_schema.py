from pydantic import BaseModel
from typing import Optional


# 🔹 Base (dữ liệu chính)
class ParentChildBase(BaseModel):
    parent_id: int
    child_id: int
    type: str  # FATHER / MOTHER
    notes: Optional[str] = None


# 🔹 Create
class ParentChildCreate(ParentChildBase):
    pass


# 🔹 Update
class ParentChildUpdate(BaseModel):
    type: Optional[str] = None
    notes: Optional[str] = None


# 🔹 Response (KHÔNG loop)
class ParentChildResponse(BaseModel):
    id: int

    parent_id: int
    parent_name: Optional[str] = None

    child_id: int
    child_name: Optional[str] = None

    type: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True