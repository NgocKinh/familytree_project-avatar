from pydantic import BaseModel
from typing import Optional, Literal


# 🔹 Base
class ParentChildBase(BaseModel):
    parent_id: int
    child_id: int
    type: Literal["father", "mother"]
    notes: Optional[str] = None


# 🔹 Create
class ParentChildCreate(ParentChildBase):
    pass


# 🔹 Update
class ParentChildUpdate(BaseModel):
    type: Optional[Literal["father", "mother"]] = None
    notes: Optional[str] = None


# 🔹 Response
class ParentChildResponse(BaseModel):
    id: int

    parent_id: int
    parent_name: Optional[str] = None

    child_id: int
    child_name: Optional[str] = None

    type: Literal["father", "mother"]
    notes: Optional[str] = None

    class Config:
        from_attributes = True