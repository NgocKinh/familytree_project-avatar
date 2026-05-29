from fastapi import Header, HTTPException, status

from backend.permissions import ROLE_KEYS


def has_permission(role: str, permission_key: str) -> bool:
    if not role:
        return False

    keys = ROLE_KEYS.get(role, [])

    if "ALL_KEYS" in keys:
        return True

    return permission_key in keys


def require_permission(permission_key: str):
    def checker(x_role: str = Header(default="viewer")):
        if not has_permission(x_role, permission_key):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền thực hiện thao tác này",
            )

        return x_role

    return checker