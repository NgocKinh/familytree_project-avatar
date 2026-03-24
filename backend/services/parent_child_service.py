from sqlalchemy.orm import Session, joinedload
from backend.models.parent_child_model import ParentChild
from backend.models.person_model import Person

from backend.api.gene_propagate import safe_propagate
from backend.utils.blood_utils import update_blood_code


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
                "parent_name": pc.parent.full_name_vn,
                "child_id": pc.child_id,
                "child_name": pc.child.full_name_vn,
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
        "parent_name": pc.parent.full_name_vn if pc.parent else None,
        "child_id": pc.child_id,
        "child_name": pc.child.full_name_vn if pc.child else None,
        "type": pc.type,
        "notes": pc.notes
    }


# ==========================================================
# 🔹 GET CHILD PARENTS STATUS
# ==========================================================
def get_child_parents_status(db: Session, child_id: int):
    rows = db.query(ParentChild.type).filter(
        ParentChild.child_id == child_id
    ).all()

    types = [r[0] for r in rows]

    return {
        "has_father": "FATHER" in types,
        "has_mother": "MOTHER" in types
    }


# ==========================================================
# 🔹 ASSIGN PARENT
# ==========================================================
def assign_parent_clean(db: Session, child_id: int, parent_id: int, ptype: str):

    if ptype not in ("FATHER", "MOTHER"):
        raise ValueError("Invalid parent type")

    if child_id == parent_id:
        raise ValueError("Parent and child cannot be the same")

    # 1️⃣ Check child
    child = db.query(Person).filter(
        Person.id == child_id,
        Person.delete_status == 0
    ).first()

    if not child:
        raise ValueError("Child not found")

    # 2️⃣ Check parent + gender
    parent = db.query(Person).filter(
        Person.id == parent_id,
        Person.delete_status == 0
    ).first()

    if not parent:
        raise ValueError("Parent not found")

    gender = (parent.gender or "").lower()

    if ptype == "FATHER" and gender != "male":
        raise ValueError("Father must be male")

    if ptype == "MOTHER" and gender != "female":
        raise ValueError("Mother must be female")

    # 3️⃣ Check duplicate
    exists = db.query(ParentChild).filter(
        ParentChild.child_id == child_id,
        ParentChild.type == ptype
    ).first()

    if exists:
        raise ValueError(f"Child already has a {ptype.lower()}")

    # 4️⃣ Insert
    pc = ParentChild(
        parent_id=parent_id,
        child_id=child_id,
        type=ptype
    )

    db.add(pc)
    db.flush()  # để lấy id nếu cần

    # 5️⃣ Propagate (giữ logic cũ)
    safe_propagate(
        conn=db.connection(),
        old_id=None,
        new_id=parent_id,
        side=ptype,
        executor="system"
    )

    update_blood_code(
        conn=db.connection(),
        child_id=child_id
    )

    db.commit()

    return pc


# ==========================================================
# 🔹 DELETE
# ==========================================================
def delete_parent_child(db: Session, rid: int):
    pc = db.query(ParentChild).filter(ParentChild.id == rid).first()

    if not pc:
        return False

    db.delete(pc)
    db.commit()

    return True