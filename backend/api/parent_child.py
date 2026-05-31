from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.services.parent_child_service import (
    get_all_parent_child,
    get_one_parent_child,
    get_child_parents_status,
    get_child_siblings,
    assign_parent_clean,
    delete_parent_child
)

from backend.schemas.parent_child_schema import ParentChildCreate
from backend.utils.auth_guard import get_current_user, has_near_access_to_any
from backend.models.user_model import User
# ✅ [CHANGE 1]: Bỏ prefix nội bộ vì main.py đã gắn prefix="/api/parent_child"
router = APIRouter(tags=["ParentChild"])

# ==========================================================
# 🔹 GET ALL
# ==========================================================
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_parent_child(db)


# ==========================================================
# 🔹 GET ONE
# ==========================================================
@router.get("/{rid}")
def get_one(rid: int, db: Session = Depends(get_db)):
    data = get_one_parent_child(db, rid)

    if not data:
        from backend.core.exceptions import NotFoundException
        raise NotFoundException("Relation not found")

    return data


# ==========================================================
# 🔹 GET CHILD PARENTS STATUS
# ==========================================================
@router.get("/child/{child_id}/parents-status")
def get_parents_status(child_id: int, db: Session = Depends(get_db)):
    return get_child_parents_status(db, child_id)

# ==========================================================
# 🔹 GET CHILD SIBLINGS
# ==========================================================
@router.get("/child/{child_id}/siblings")
def get_siblings_of_child(child_id: int, db: Session = Depends(get_db)):
    return get_child_siblings(db, child_id)

# ==========================================================
# 🔹 ASSIGN PARENT
# ==========================================================
@router.post("/assign", status_code=201)
def assign_parent(
    data: ParentChildCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not has_near_access_to_any(
        current_user,
        [data.child_id, data.parent_id],
        "relation:create"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền thêm/chỉnh sửa quan hệ cha con này",
        )

    pc = assign_parent_clean(
        db,
        child_id=data.child_id,
        parent_id=data.parent_id,
        ptype=data.type
    )

    return {
        "message": "Parent assigned successfully",
        "id": pc.id
    }

# ==========================================================
# 🔹 DELETE
# ==========================================================
@router.delete("/{rid}")
def delete_relation(rid: int, db: Session = Depends(get_db)):
    delete_parent_child(db, rid)

    return {"message": "Deleted successfully"}