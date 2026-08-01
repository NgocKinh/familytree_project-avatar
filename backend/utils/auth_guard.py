from fastapi import Depends, HTTPException, status
from backend.api.auth import get_current_user
from backend.models.user_model import User
from backend.permissions import ROLE_KEYS
from backend.domain.engine_v2.relationship_resolver import resolver_relationship

import time

NEAR_RELATION_VIEW = {
    "self",
    "spouse",
    "parent",
    "child",
    "sibling",
    "grandparent",
    "grandchild",
    "uncle_aunt",
    "nephew_niece",
    "sibling_in_law"
}
NEAR_RELATION_EDIT = {
    "self",
    "spouse",
    "parent",
    "child",
    "sibling",
    "uncle_aunt",
}
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

def is_near_person(
    current_user: User,
    target_person_id: int,
    permission_key: str = "relation:create",
) -> bool:
    if current_user.person_id is None:
        return False

    if current_user.person_id == target_person_id:
        return True

    t0 = time.perf_counter()

    result = resolver_relationship(
        current_user.person_id,
        target_person_id
    )

    print(
        f"🔥 resolver_relationship: {time.perf_counter()-t0:.3f}s"
    )

    relation_basic = None
    relation_label = None

    if result:
        standard_result = result.get("result") or {}

        relation_basic = (
            standard_result.get("relation_basic")
            or result.get("relation_basic")
            or result.get("relationship")
        )

        relation_label = (
            standard_result.get("relation")
            or result.get("relation")
        )

    if permission_key in {
        "relation:create",
        "relation:update",
        "birth_order:update",
    }:
        return relation_basic in NEAR_RELATION_EDIT

    return relation_basic in NEAR_RELATION_VIEW

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
        if is_near_person(
            current_user,
            int(target_person_id),
            permission_key,
        ):
            return True

    return False