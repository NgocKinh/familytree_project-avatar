from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.api.auth import get_current_user
from backend.db import get_db
from backend.models.audit_log_model import AuditLog
from backend.models.user_model import User


router = APIRouter(tags=["Audit Log"])


@router.get("")
def list_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    username: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Chỉ Admin được xem Audit Log.",
        )

    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)

    if entity_id is not None:
        query = query.filter(AuditLog.entity_id == entity_id)

    if username:
        query = query.filter(AuditLog.username.ilike(f"%{username.strip()}%"))

    total = query.count()

    rows = (
        query
        .order_by(AuditLog.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "success": True,
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": [
            {
                "id": row.id,
                "user_id": row.user_id,
                "username": row.username,
                "role": row.role,
                "action": row.action,
                "entity_type": row.entity_type,
                "entity_id": row.entity_id,
                "description": row.description,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }