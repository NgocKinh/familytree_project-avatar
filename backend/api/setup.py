import os
import re
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field

from backend.api.auth import create_access_token, get_current_user
from backend.db import get_connection
from backend.models.user_model import User
from backend.password_utils import hash_password

router = APIRouter(tags=["Setup"])

DEFAULT_BACKGROUND_IMAGE = "/trongdong.png"
MAX_BACKGROUND_DATA_LENGTH = 3_000_000
BACKGROUND_DATA_PATTERN = re.compile(
    r"^data:image/(?:png|jpeg|webp);base64,[A-Za-z0-9+/=]+$"
)

class FamilyConfigRequest(BaseModel):
    family_code: str = Field(min_length=2, max_length=50)
    family_name: str = Field(min_length=3, max_length=255)
    signboard: str = Field(min_length=3, max_length=255)
    subtitle: str = Field(default="", max_length=255)
    slogan_line_1: str = Field(default="", max_length=255)
    slogan_line_2: str = Field(default="", max_length=255)
    origin_line: str = Field(default="", max_length=255)
    welcome_title: str = Field(default="", max_length=255)
    welcome_text: str = Field(default="", max_length=2000)
    background_image: str = Field(
        default=DEFAULT_BACKGROUND_IMAGE,
        max_length=MAX_BACKGROUND_DATA_LENGTH,
    )


class SetupCompleteRequest(FamilyConfigRequest):
    admin_username: str = Field(
        min_length=3,
        max_length=100,
        pattern=r"^[A-Za-z0-9_.-]+$",
    )
    admin_password: str = Field(min_length=8, max_length=72)
    admin_full_name: str = Field(min_length=2, max_length=255)


def _default_config():
    return {
        "familyCode": "FamilyTree",
        "familyName": "Gia Ph\u1ea3 D\u00f2ng H\u1ecd",
        "signboard": "GIA PH\u1ea2 D\u00d2NG H\u1ecc",
        "subtitle": "G\u00ecn Gi\u1eef C\u1ed9i Ngu\u1ed3n",
        "sloganLines": [
            "K\u1ebft N\u1ed1i C\u00e1c Th\u1ebf H\u1ec7",
            "G\u00ecn Gi\u1eef Truy\u1ec1n Th\u1ed1ng",
        ],
        "originLine": "T\u00ean d\u00f2ng h\u1ecd \u2013 Qu\u00ea qu\u00e1n",
        "welcomeTitle": "Ch\u00e0o m\u1eebng b\u1ea1n \u0111\u1ebfn v\u1edbi h\u1ec7 th\u1ed1ng gia ph\u1ea3",
        "welcomeText": (
            "N\u01a1i l\u01b0u gi\u1eef truy\u1ec1n th\u1ed1ng, k\u1ebft n\u1ed1i "
            "c\u00e1c th\u1ebf h\u1ec7 v\u00e0 t\u00f4n vinh c\u1ed9i ngu\u1ed3n."
        ),
        "backgroundImage": DEFAULT_BACKGROUND_IMAGE,
        "navbarIcon": "\U0001F4DC",
    }


def _system_is_configured(cursor):
    cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1
            FROM users
            WHERE role = 'admin'
            LIMIT 1
        ) AS has_admin
        """
    )
    has_admin = bool(cursor.fetchone()["has_admin"])

    cursor.execute(
        """
        SELECT EXISTS(
            SELECT 1
            FROM family_settings
            WHERE id = 1
            LIMIT 1
        ) AS has_settings
        """
    )
    has_settings = bool(cursor.fetchone()["has_settings"])

    return has_admin or has_settings


def _clean_payload(payload):
    return {
        key: value.strip()
        for key, value in payload.model_dump().items()
    }


def _validate_family_config(cleaned):
    required_values = (
        cleaned["family_code"],
        cleaned["family_name"],
        cleaned["signboard"],
    )

    if not all(required_values):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Required family configuration fields cannot be blank.",
        )

    background_image = (
        cleaned.get("background_image") or DEFAULT_BACKGROUND_IMAGE
    )

    if (
        background_image != DEFAULT_BACKGROUND_IMAGE
        and not BACKGROUND_DATA_PATTERN.fullmatch(background_image)
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Background image must be PNG, JPG, or WebP.",
        )

    cleaned["background_image"] = background_image
    return cleaned


@router.get("/status")
def setup_status():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        configured = _system_is_configured(cursor)
        setup_enabled = (
            not configured
            and bool(os.getenv("SETUP_TOKEN", "").strip())
        )

        return {
            "configured": configured,
            "requiresSetup": not configured,
            "setupEnabled": setup_enabled,
        }
    finally:
        cursor.close()
        connection.close()


@router.get("/config")
def public_family_config():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                family_code,
                family_name,
                signboard,
                subtitle,
                slogan_line_1,
                slogan_line_2,
                origin_line,
                welcome_title,
                welcome_text,
                background_image,
                navbar_icon
            FROM family_settings
            WHERE id = 1
            LIMIT 1
            """
        )
        row = cursor.fetchone()

        if not row:
            return _default_config()

        return {
            "familyCode": row["family_code"],
            "familyName": row["family_name"],
            "signboard": row["signboard"],
            "subtitle": row["subtitle"] or "",
            "sloganLines": [
                row["slogan_line_1"] or "",
                row["slogan_line_2"] or "",
            ],
            "originLine": row["origin_line"] or "",
            "welcomeTitle": row["welcome_title"] or "",
            "welcomeText": row["welcome_text"] or "",
            "backgroundImage": (
                row["background_image"] or DEFAULT_BACKGROUND_IMAGE
            ),
            "navbarIcon": row["navbar_icon"] or "\U0001F4DC",
        }
    finally:
        cursor.close()
        connection.close()


@router.post("/complete", status_code=status.HTTP_201_CREATED)
def complete_setup(
    payload: SetupCompleteRequest,
    x_setup_token: str | None = Header(default=None, alias="X-Setup-Token"),
):
    expected_token = os.getenv("SETUP_TOKEN", "").strip()

    if not expected_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="SETUP_TOKEN is not configured.",
        )

    if not x_setup_token or not secrets.compare_digest(
        x_setup_token,
        expected_token,
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid setup token.",
        )

    cleaned = _validate_family_config(_clean_payload(payload))

    required_values = (
        cleaned["admin_username"],
        cleaned["admin_password"],
        cleaned["admin_full_name"],
    )

    if not all(required_values):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Required setup fields cannot be blank.",
        )

    try:
        password_hash = hash_password(cleaned["admin_password"])
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        if _system_is_configured(cursor):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Setup is already completed.",
            )

        cursor.execute(
            """
            INSERT INTO family_settings (
                id,
                family_code,
                family_name,
                signboard,
                subtitle,
                slogan_line_1,
                slogan_line_2,
                origin_line,
                welcome_title,
                welcome_text,
                background_image,
                navbar_icon
            )
            VALUES (
                1, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, NULL
            )
            """,
            (
                cleaned["family_code"],
                cleaned["family_name"],
                cleaned["signboard"],
                cleaned["subtitle"],
                cleaned["slogan_line_1"],
                cleaned["slogan_line_2"],
                cleaned["origin_line"],
                cleaned["welcome_title"],
                cleaned["welcome_text"],
                cleaned["background_image"],
            ),
        )

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password_hash,
                full_name,
                role,
                is_active,
                person_id,
                created_at
            )
            VALUES (
                %s, %s, %s, 'admin', 1, NULL, CURRENT_TIMESTAMP
            )
            """,
            (
                cleaned["admin_username"],
                password_hash,
                cleaned["admin_full_name"],
            ),
        )

        admin_id = cursor.lastrowid
        admin_user = {
            "id": admin_id,
            "username": cleaned["admin_username"],
            "full_name": cleaned["admin_full_name"],
            "role": "admin",
            "person_id": None,
        }
        access_token = create_access_token(
            {
                "sub": str(admin_id),
                "username": cleaned["admin_username"],
                "role": "admin",
            }
        )

        connection.commit()

        return {
            "success": True,
            "message": "FamilyTree setup completed.",
            "access_token": access_token,
            "token_type": "bearer",
            "user": admin_user,
        }
    except HTTPException:
        connection.rollback()
        raise
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


@router.put("/config")
def update_family_config(
    payload: FamilyConfigRequest,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin can update family configuration.",
        )

    cleaned = _validate_family_config(_clean_payload(payload))
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT 1 FROM family_settings WHERE id = 1 LIMIT 1"
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Family configuration was not found.",
            )

        cursor.execute(
            """
            UPDATE family_settings
            SET
                family_code = %s,
                family_name = %s,
                signboard = %s,
                subtitle = %s,
                slogan_line_1 = %s,
                slogan_line_2 = %s,
                origin_line = %s,
                welcome_title = %s,
                welcome_text = %s,
                background_image = %s
            WHERE id = 1
            """,
            (
                cleaned["family_code"],
                cleaned["family_name"],
                cleaned["signboard"],
                cleaned["subtitle"],
                cleaned["slogan_line_1"],
                cleaned["slogan_line_2"],
                cleaned["origin_line"],
                cleaned["welcome_title"],
                cleaned["welcome_text"],
                cleaned["background_image"],
            ),
        )

        connection.commit()

        return {
            "success": True,
            "message": "Family configuration updated.",
        }
    except HTTPException:
        connection.rollback()
        raise
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
