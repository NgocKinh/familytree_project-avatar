from fastapi import Depends, HTTPException, status

from backend.api.auth import get_current_user, NEAR_RELATION_BASICS
from backend.models.user_model import User
from backend.permissions import ROLE_KEYS
from backend.domain.engine_v2.relationship_resolver import resolver_relationship

def has_permission(role: str, permission_key: str) -> bool:
    if not role:
        return False

    keys = ROLE_KEYS.get(role, [])

    if "ALL_KEYS" in keys:
        return True

    return permission_key in keys

def require_permission(permission_key: str):
    def checker(current_user: User = Depends(get_current_user)):
        if not has_permission(current_user.role, permission_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền thực hiện thao tác này",
            )

        return current_user

    return checker

# ==========================================================
# DYNAMIC CLOSE MEMBER — NEAR ACCESS HELPERS
# Dùng chung cho Marriage, ParentChild, FamilySetup
# ==========================================================

def is_near_person(current_user: User, target_person_id: int) -> bool:
    if current_user.person_id is None:
        return False

    if current_user.person_id == target_person_id:
        return True

    result = resolver_relationship(
        current_user.person_id,
        target_person_id
    )

    relation_basic = None

    if result:
        relation_basic = (
            result.get("result", {}).get("relation_basic")
            or result.get("relation_basic")
            or result.get("relationship")
        )

    return relation_basic in NEAR_RELATION_BASICS


def has_near_access_to_any(
    current_user: User,
    target_person_ids: list[int],
    permission_key: str = "relation:create"
) -> bool:
    if has_permission(current_user.role, permission_key):
        return True

    if current_user.role != "member_basic":
        return False

    for target_person_id in target_person_ids:
        if is_near_person(current_user, int(target_person_id)):
            return True

    return False