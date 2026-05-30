from fastapi import Depends, HTTPException, status

from backend.api.auth import get_current_user
from backend.models.user_model import User
from backend.permissions import ROLE_KEYS


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