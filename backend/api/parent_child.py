# ==========================================================
# File: backend/api/parent_child.py (ORM VERSION)
# ==========================================================

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.services.parent_child_service import (
    get_all_parent_child,
    get_one_parent_child,
    get_child_parents_status,
    assign_parent_clean,
    delete_parent_child
)

router = APIRouter()


# ==========================================================
# 🔹 GET ALL
# ==========================================================
@router.get("/api/parent_child")
def get_all(db: Session = Depends(get_db)):
    try:
        return get_all_parent_child(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# 🔹 GET ONE
# ==========================================================
@router.get("/api/parent_child/{rid}")
def get_one(rid: int, db: Session = Depends(get_db)):
    try:
        data = get_one_parent_child(db, rid)

        if not data:
            raise HTTPException(status_code=404, detail="Relation not found")

        return data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# 🔹 GET CHILD PARENTS STATUS
# ==========================================================
@router.get("/api/child/{child_id}/parents-status")
def get_parents_status(child_id: int, db: Session = Depends(get_db)):
    try:
        return get_child_parents_status(db, child_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# 🔹 ASSIGN PARENT
# ==========================================================
@router.post("/api/parent_child/assign", status_code=201)
def assign_parent(payload: dict, db: Session = Depends(get_db)):
    try:
        child_id = payload.get("child_id")
        parent_id = payload.get("parent_id")
        ptype = payload.get("type")

        if not child_id or not parent_id or not ptype:
            raise HTTPException(status_code=400, detail="Missing required fields")

        pc = assign_parent_clean(db, child_id, parent_id, ptype)

        return {
            "message": "Parent assigned successfully",
            "id": pc.id
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        if "duplicate" in str(e).lower():
            raise HTTPException(status_code=409, detail="Parent already assigned")

        raise HTTPException(status_code=500, detail=str(e))


# ==========================================================
# 🔹 DELETE
# ==========================================================
@router.delete("/api/parent_child/{rid}")
def delete_relation(rid: int, db: Session = Depends(get_db)):
    try:
        ok = delete_parent_child(db, rid)

        if not ok:
            raise HTTPException(status_code=404, detail="Relation not found")

        return {"message": "Deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))