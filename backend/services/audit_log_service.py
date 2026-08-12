from backend.models.audit_log_model import AuditLog


def write_audit_log(
    db,
    current_user,
    action,
    entity_type,
    entity_id=None,
    description=None,
):
    audit_log = AuditLog(
        user_id=current_user.id,
        username=current_user.username,
        role=current_user.role,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )

    db.add(audit_log)
    db.flush()

    return audit_log