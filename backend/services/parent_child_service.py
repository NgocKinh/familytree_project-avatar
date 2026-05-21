from sqlalchemy.orm import Session, joinedload
from backend.models.parent_child_model import ParentChild
from backend.models.person_model import Person

from backend.api.gene_propagate import safe_propagate
from backend.utils.blood_utils import update_blood_code
from backend.core.exceptions import NotFoundException, BadRequestException


# ==========================================================
# 🔹 GET ALL
# ==========================================================
def get_all_parent_child(db: Session):
    records = (
        db.query(ParentChild)
        .options(
            joinedload(ParentChild.parent),
            joinedload(ParentChild.child)
        )
        .order_by(ParentChild.id.asc())
        .all()
    )

    result = []
    for pc in records:
        if pc.parent and pc.child:
            result.append({
                "id": pc.id,

                "parent_id": pc.parent_id,
                "parent_name": pc.parent.full_name if pc.parent else None,

                # ✅ [ADDED]: object chuẩn cho frontend
                "parent": {
                    "id": pc.parent.id,
                    "sur_name": pc.parent.sur_name,
                    "last_name": pc.parent.last_name,
                    "middle_name": pc.parent.middle_name,
                    "first_name": pc.parent.first_name,
                    "gender": pc.parent.gender.value if pc.parent.gender else None
                } if pc.parent else None,

                "child_id": pc.child_id,
                "child_name": pc.child.full_name if pc.child else None,

                # ✅ [ADDED]
                "child": {
                    "id": pc.child.id,
                    "sur_name": pc.child.sur_name,
                    "last_name": pc.child.last_name,
                    "middle_name": pc.child.middle_name,
                    "first_name": pc.child.first_name,
                    "gender": pc.child.gender.value if pc.child.gender else None
                } if pc.child else None,

                "type": pc.type,
                "notes": pc.notes
            })

    return result


# ==========================================================
# 🔹 GET ONE
# ==========================================================
def get_one_parent_child(db: Session, rid: int):
    pc = (
        db.query(ParentChild)
        .options(
            joinedload(ParentChild.parent),
            joinedload(ParentChild.child)
        )
        .filter(ParentChild.id == rid)
        .first()
    )

    if not pc:
        return None

    return {
    "id": pc.id,

    "parent_id": pc.parent_id,
    "parent_name": pc.parent.full_name if pc.parent else None,
    "parent": {
        "id": pc.parent.id,
        "sur_name": pc.parent.sur_name,
        "last_name": pc.parent.last_name,
        "middle_name": pc.parent.middle_name,
        "first_name": pc.parent.first_name,
        "gender": pc.parent.gender.value if pc.parent.gender else None
    } if pc.parent else None,

    "child_id": pc.child_id,
    "child_name": pc.child.full_name if pc.child else None,
    "child": {
        "id": pc.child.id,
        "sur_name": pc.child.sur_name,
        "last_name": pc.child.last_name,
        "middle_name": pc.child.middle_name,
        "first_name": pc.child.first_name,
        "gender": pc.child.gender.value if pc.child.gender else None
    } if pc.child else None,

    "type": pc.type,
    "notes": pc.notes
}

# ==========================================================
# 🔹 GET CHILD PARENTS STATUS
# ==========================================================
def get_child_parents_status(db: Session, child_id: int):

    records = (
        db.query(ParentChild)
        .options(joinedload(ParentChild.parent))   # 📌 load parent
        .filter(ParentChild.child_id == child_id)
        .all()
    )

    father = None
    mother = None

    for pc in records:
        ptype = (pc.type or "").strip().lower()

        if ptype == "father" and not father:   # 📌 chống duplicate
            father = {
                "id": pc.parent_id,
                "name": pc.parent.full_name if pc.parent else None
            }

        elif ptype == "mother" and not mother:
            mother = {
                "id": pc.parent_id,
                "name": pc.parent.full_name if pc.parent else None
            }

    return {
        "father": father,
        "mother": mother
    }

# ==========================================================
# 🔹 ASSIGN PARENT
# ==========================================================
def assign_parent_clean(db: Session, child_id: int, parent_id: int, ptype: str):

    if ptype not in ("father", "mother"):
        raise BadRequestException("Invalid parent type")

    if child_id == parent_id:
        raise BadRequestException("Parent and child cannot be the same")

    # 1️⃣ Check child
    child = db.query(Person).filter(
        Person.id == child_id,
        Person.delete_status == 0
    ).first()

    if not child:
        raise NotFoundException("Child not found")

    # 2️⃣ Check parent + gender
    parent = db.query(Person).filter(
        Person.id == parent_id,
        Person.delete_status == 0
    ).first()

    if not parent:
        raise NotFoundException("Parent not found")

    gender = (parent.gender or "").lower()

    ptype = (ptype or "").strip().lower()

    if ptype == "father" and gender != "male":
        raise BadRequestException("Father must be male")

    if ptype == "mother" and gender != "female":
        raise BadRequestException("Mother must be female")

    # 3️⃣ Check duplicate (business rule: 1 father / 1 mother)
    exists = db.query(ParentChild).filter(
        ParentChild.child_id == child_id,
        ParentChild.type == ptype
    ).first()

    if exists:
        raise BadRequestException(f"Child already has a {ptype.lower()}")

    # 🔥 Extra duplicate check (same relation)
    dup = db.query(ParentChild).filter(
        ParentChild.parent_id == parent_id,
        ParentChild.child_id == child_id,
        ParentChild.type == ptype
    ).first()

    if dup:
        raise BadRequestException("Relationship already exists")

    # 4️⃣ Insert + transaction safety
    try:
        pc = ParentChild(
            parent_id=parent_id,
            child_id=child_id,
            type=ptype
        )

        db.add(pc)
        db.flush()

        # 5️⃣ Propagate (giữ nguyên logic domain)
        safe_propagate(
            conn=db.connection().connection,
            old_id=None,
            new_id=parent_id,
            side=ptype,
            executor="system"
        )

        update_blood_code(
            conn=db.connection().connection,
            child_id=child_id
        )

        db.commit()

    except Exception:
        db.rollback()
        raise

    return pc

# ==========================================================
# 🔹 DELETE
# ==========================================================
def delete_parent_child(db: Session, rid: int):
    pc = db.query(ParentChild).filter(ParentChild.id == rid).first()

    if not pc:
        raise NotFoundException("Relationship not found")

    db.delete(pc)
    db.commit()

    return True