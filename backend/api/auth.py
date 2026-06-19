from datetime import datetime, timedelta
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.models.user_model import User
from backend.domain.engine_v2.relationship_resolver import resolver_relationship

router = APIRouter(tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_FAMILYTREE_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 8))
NEAR_RELATION_BASICS = {
    "self",
    "spouse",
    "parent",
    "child",
    "sibling",
    "grandparent",
    "grandchild",
    "uncle_aunt",
    "nephew_niece",
}
NEAR_RELATION_EDIT = {
    "self",
    "spouse",
    "parent",
    "child",
    "sibling",
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class LoginRequest(BaseModel):
    username: str
    password: str

class CheckNearRequest(BaseModel):
    target_person_id: int
    action: str = "relation:create"

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Đăng nhập không hợp lệ. Vui lòng đăng nhập lại.",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản không tồn tại hoặc đã bị xoá.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khoá",
        )

    return user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khoá",
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu",
        )
 
    access_token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "person_id": user.person_id,
        }
    }
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "person_id": current_user.person_id,
    }  

@router.post("/check-near-access")
def check_near_access(
    data: CheckNearRequest,
    current_user: User = Depends(get_current_user)
):
    if current_user.role in ["admin", "co_operator"]:
        return {
            "allowed": True,
            "effective_role": current_user.role,
            "reason": "Vai trò có quyền nhập liệu không cần xét quan hệ gần",
            "current_person_id": current_user.person_id,
            "target_person_id": data.target_person_id,
            "relationship": None,
        }

    if current_user.person_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản chưa được liên kết với thành viên gia phả. Vui lòng liên hệ quản trị viên.",
        )

    if current_user.person_id == data.target_person_id:
        return {
            "allowed": True,
            "effective_role": "member_close",
            "reason": "Chính bản thân người dùng",
            "current_person_id": current_user.person_id,
            "target_person_id": data.target_person_id,
            "relationship": "self",
        }

    result = resolver_relationship(
        current_user.person_id,
        data.target_person_id
    )
    relation_basic = None

    if result:
        relation_basic = (
            result.get("result", {}).get("relation_basic")
            or result.get("relation_basic")
            or result.get("relationship")
        )

    if data.action in ["relation:create", "relation:update", "birth_order:update"]:
        allowed = relation_basic in NEAR_RELATION_EDIT
    else:
        allowed = relation_basic in NEAR_RELATION_BASICS

    return {
    "allowed": allowed,
    "effective_role": "member_close" if allowed else current_user.role,
    "reason": "Có quan hệ gần" if allowed else "Không có mối quan hệ gần với người được thêm hoặc chỉnh sửa",
    "current_person_id": current_user.person_id,
    "target_person_id": data.target_person_id,
    "relation_basic": relation_basic,
    "relationship": result,
}  