from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
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
from backend.models.marriage_model import Marriage
from backend.models.parent_child_model import ParentChild
from backend.models.person_model import Person
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
        raise NotFoundException("Không tìm thấy quan hệ cha-con này")

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
# 🔹 GET CHILDREN BY MARRIAGE
# ==========================================================
@router.get("/marriage/{marriage_id}/children")
def get_children_by_marriage(marriage_id: int, db: Session = Depends(get_db)):
    marriage = db.query(Marriage).filter(Marriage.id == marriage_id).first()

    if not marriage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy gia đình/hôn nhân",
        )

    parent_ids = [marriage.spouse_a_id, marriage.spouse_b_id]

    rows = (
        db.query(Person)
        .join(ParentChild, ParentChild.child_id == Person.id)
        .filter(ParentChild.parent_id.in_(parent_ids))
        .all()
    )

    return rows
# ==========================================================
# 🔹 GET COMMON CHILDREN BY PARENT PAIR
# ==========================================================
@router.get("/parents/{father_id}/{mother_id}/children")
def get_common_children_by_parent_pair(
    father_id: int,
    mother_id: int,
    db: Session = Depends(get_db),
):
    parent_ids = [father_id, mother_id]

    rows = (
        db.query(Person)
        .join(ParentChild, ParentChild.child_id == Person.id)
        .filter(ParentChild.parent_id.in_(parent_ids))
        .group_by(Person.id)
        .having(func.count(func.distinct(ParentChild.parent_id)) == 2)
        .all()
    )

    return rows    
# ==========================================================
# 🔹 ASSIGN PARENT
# ==========================================================
@router.post("/assign", status_code=201)
def assign_parent(
    data: ParentChildCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["admin", "co_operator"]:
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
        "message": "Đã lưu quan hệ cha-con thành công",
        "id": pc.id
    }

# ==========================================================
# 🔹 DELETE
# ==========================================================
@router.delete("/{rid}")
def delete_relation(rid: int, db: Session = Depends(get_db)):
    delete_parent_child(db, rid)

    return {"message": "Đã xóa quan hệ cha-con thành công"}