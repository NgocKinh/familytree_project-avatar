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
# 🔧 PERSON SUMMARY
# ==========================================================
def person_summary(p: Person):
    if not p:
        return None

    return {
        "id": p.id,
        "sur_name": p.sur_name,
        "last_name": p.last_name,
        "middle_name": p.middle_name,
        "first_name": p.first_name,
        "full_name_vn": getattr(p, "full_name_vn", None),
        "gender": p.gender,
        "birth_date": str(p.birth_date) if p.birth_date else None,
        "birth_order": p.birth_order,
    }

def get_parent_map(db: Session, child_id: int):
    rows = (
        db.query(ParentChild, Person)
        .join(Person, ParentChild.parent_id == Person.id)
        .filter(ParentChild.child_id == child_id)
        .all()
    )

    father = None
    mother = None

    for pc, parent in rows:
        ptype = (pc.type or "").lower()

        if ptype in ["father", "cha"]:
            father = parent

        if ptype in ["mother", "me", "mẹ"]:
            mother = parent

    return father, mother
# ==========================================================
# 🔹 GET ALL
# ==========================================================
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_parent_child(db)
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
# 🔹 GET PERSON FAMILY OVERVIEW
# ==========================================================
@router.get("/person/{person_id}/family")
def get_person_family_overview(
    person_id: int,
    db: Session = Depends(get_db),
):
    person = db.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thành viên",
        )

    def sort_people(rows):
        return sorted(
            rows,
            key=lambda p: (
                p.get("birth_order") or 9999,
                p.get("birth_date") or "9999-99-99",
                p.get("id") or 999999,
            ),
        )

    # ======================================================
    # 1️⃣ HÔN NHÂN CỦA NHÂN VẬT TRUNG TÂM
    # ======================================================
    marriages = (
        db.query(Marriage)
        .filter(
            (Marriage.spouse_a_id == person_id)
            | (Marriage.spouse_b_id == person_id)
        )
        .all()
    )

    marriage_overview = []

    for marriage in marriages:
        spouse_id = (
            marriage.spouse_b_id
            if marriage.spouse_a_id == person_id
            else marriage.spouse_a_id
        )

        spouse = db.query(Person).filter(Person.id == spouse_id).first()

        parent_ids = [marriage.spouse_a_id, marriage.spouse_b_id]

        children = (
            db.query(Person)
            .join(ParentChild, ParentChild.child_id == Person.id)
            .filter(ParentChild.parent_id.in_(parent_ids))
            .group_by(Person.id)
            .having(func.count(func.distinct(ParentChild.parent_id)) == 2)
            .all()
        )

        marriage_overview.append(
            {
                "marriage_id": marriage.id,
                "spouse": person_summary(spouse),
                "children": sort_people(
                    [person_summary(child) for child in children]
                ),
            }
        )

    # ======================================================
    # 2️⃣ ANH CHỊ EM ĐẶC BIỆT CỦA NHÂN VẬT TRUNG TÂM
    # ======================================================
    father, mother = get_parent_map(db, person_id)

    father_id = father.id if father else None
    mother_id = mother.id if mother else None

    sibling_ids = set()

    if father_id:
        rows = (
            db.query(ParentChild)
            .filter(
                ParentChild.parent_id == father_id,
                ParentChild.child_id != person_id,
            )
            .all()
        )

        for row in rows:
            sibling_ids.add(row.child_id)

    if mother_id:
        rows = (
            db.query(ParentChild)
            .filter(
                ParentChild.parent_id == mother_id,
                ParentChild.child_id != person_id,
            )
            .all()
        )

        for row in rows:
            sibling_ids.add(row.child_id)

    same_father_different_mother = []
    same_mother_different_father = []
    known_same_father_only = []
    known_same_mother_only = []

    for sibling_id in sibling_ids:
        sibling = db.query(Person).filter(Person.id == sibling_id).first()

        if not sibling:
            continue

        sib_father, sib_mother = get_parent_map(db, sibling_id)

        sib_father_id = sib_father.id if sib_father else None
        sib_mother_id = sib_mother.id if sib_mother else None

        same_father = father_id is not None and father_id == sib_father_id
        same_mother = mother_id is not None and mother_id == sib_mother_id

        # Không liệt kê cùng cha cùng mẹ
        if same_father and same_mother:
            continue

        if same_father:
            if mother_id and sib_mother_id and mother_id != sib_mother_id:
                same_father_different_mother.append(person_summary(sibling))
            else:
                known_same_father_only.append(person_summary(sibling))

        elif same_mother:
            if father_id and sib_father_id and father_id != sib_father_id:
                same_mother_different_father.append(person_summary(sibling))
            else:
                known_same_mother_only.append(person_summary(sibling))

    return {
        "person": person_summary(person),
        "marriages": marriage_overview,
        "special_siblings": {
            "same_father_different_mother": sort_people(
                same_father_different_mother
            ),
            "same_mother_different_father": sort_people(
                same_mother_different_father
            ),
            "known_same_father_only": sort_people(
                known_same_father_only
            ),
            "known_same_mother_only": sort_people(
                known_same_mother_only
            ),
        },
    }
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