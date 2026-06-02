from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.db import get_db
from backend.models.user_model import User
from backend.schemas.user_schema import UserCreate, UserUpdate
from backend.api.auth import get_current_user


router = APIRouter(tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def require_admin(current_user: User):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới có quyền quản lý tài khoản",
        )


@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    users = db.query(User).order_by(User.id.asc()).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "person_id": user.person_id,
            "is_active": user.is_active,
            "created_at": user.created_at,
        }
        for user in users
    ]


@router.post("/", status_code=201)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    existing = db.query(User).filter(User.username == data.username).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username đã tồn tại",
        )
    # ==================================================
    # 1 PERSON = 1 USER
    # ==================================================
    if data.person_id is not None:

        existing_person = (
            db.query(User)
            .filter(User.person_id == data.person_id)
            .first()
        )

        if existing_person:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Thành viên này đã có tài khoản user"
            )
    
    user = User(
        username=data.username,
        password_hash=pwd_context.hash(data.password),
        full_name=data.full_name,
        role=data.role,
        person_id=data.person_id,
        is_active=data.is_active,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Tạo tài khoản thành công",
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }


@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user",
        )

    if data.password:
        user.password_hash = pwd_context.hash(data.password)

    if data.full_name is not None:
        user.full_name = data.full_name

    if data.role is not None:
        user.role = data.role

    if data.person_id is not None:
        user.person_id = data.person_id

    if data.is_active is not None:
        user.is_active = data.is_active

    db.commit()
    db.refresh(user)

    return {
        "message": "Cập nhật tài khoản thành công",
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active,
    }

@router.put("/{user_id}/lock")
def lock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể tự khóa tài khoản đang đăng nhập",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user",
        )

    user.is_active = False
    db.commit()

    return {"message": "Đã khóa tài khoản", "id": user.id}


@router.put("/{user_id}/unlock")
def unlock_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user",
        )

    user.is_active = True
    db.commit()

    return {"message": "Đã mở khóa tài khoản", "id": user.id}

@router.put("/{user_id}/reset-password")
def reset_password(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if not data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password mới không được để trống",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user",
        )

    user.password_hash = pwd_context.hash(data.password)
    db.commit()

    return {"message": "Reset password thành công", "id": user.id}

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể tự xóa tài khoản đang đăng nhập",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy user",
        )

    db.delete(user)
    db.commit()

    return {
        "message": "Xóa tài khoản thành công",
        "id": user_id,
    }