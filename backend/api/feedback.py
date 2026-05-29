# ======================================================
# API: Feedback (v1.0-PRIVATE-SUPPORT)
# ======================================================
# - User gửi góp ý / báo lỗi / trở ngại
# - Không công khai
# - Admin đọc và xử lý nội bộ
# - Phase 1: CRUD cơ bản + status workflow
# ======================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.db import get_connection

router = APIRouter()


# ======================================================
# SAFE CLOSE
# ======================================================
def safe_close(conn, cursor):
    try:
        if cursor:
            cursor.close()
    except Exception as e:
        print("⚠️ Cursor close error:", e)

    try:
        if conn:
            conn.close()
    except Exception as e:
        print("⚠️ Connection close error:", e)


# ======================================================
# SCHEMAS
# ======================================================
class FeedbackCreate(BaseModel):
    user_id: Optional[int] = None
    category: str
    title: str
    message: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class FeedbackUpdate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    message: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[str] = None
    admin_note: Optional[str] = None


# ======================================================
# CREATE FEEDBACK
# User gửi feedback
# ======================================================
@router.post("/create")
def create_feedback(payload: FeedbackCreate):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            INSERT INTO feedback (
                user_id,
                category,
                title,
                message,
                contact_email,
                contact_phone,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s, 'new')
        """, (
            payload.user_id,
            payload.category,
            payload.title,
            payload.message,
            payload.contact_email,
            payload.contact_phone,
        ))

        conn.commit()

        return {
            "success": True,
            "message": "Feedback created successfully",
            "feedback_id": cursor.lastrowid
        }

    except Exception as e:
        print("❌ CREATE FEEDBACK ERROR:", e)
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        safe_close(conn, cursor)


# ======================================================
# LIST FEEDBACK
# Admin xem danh sách feedback
# ======================================================
@router.get("/list")
def list_feedback():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                feedback_id,
                user_id,
                category,
                title,
                message,
                contact_email,
                contact_phone,
                status,
                admin_note,
                created_at,
                updated_at
            FROM feedback
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        return {
            "success": True,
            "feedbacks": rows
        }

    except Exception as e:
        print("❌ LIST FEEDBACK ERROR:", e)
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        safe_close(conn, cursor)


# ======================================================
# DETAIL FEEDBACK
# Admin xem chi tiết 1 feedback
# ======================================================
@router.get("/{feedback_id}")
def get_feedback(feedback_id: int):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                feedback_id,
                user_id,
                category,
                title,
                message,
                contact_email,
                contact_phone,
                status,
                admin_note,
                created_at,
                updated_at
            FROM feedback
            WHERE feedback_id = %s
        """, (feedback_id,))

        row = cursor.fetchone()

        if not row:
            return {
                "success": False,
                "message": "Feedback not found"
            }

        return {
            "success": True,
            "feedback": row
        }

    except Exception as e:
        print("❌ GET FEEDBACK ERROR:", e)
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        safe_close(conn, cursor)


# ======================================================
# UPDATE FEEDBACK
# Admin cập nhật status / admin_note
# ======================================================
@router.put("/{feedback_id}")
def update_feedback(feedback_id: int, payload: FeedbackUpdate):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            UPDATE feedback
            SET
                category = COALESCE(%s, category),
                title = COALESCE(%s, title),
                message = COALESCE(%s, message),
                contact_email = COALESCE(%s, contact_email),
                contact_phone = COALESCE(%s, contact_phone),
                status = COALESCE(%s, status),
                admin_note = COALESCE(%s, admin_note)
            WHERE feedback_id = %s
        """, (
            payload.category,
            payload.title,
            payload.message,
            payload.contact_email,
            payload.contact_phone,
            payload.status,
            payload.admin_note,
            feedback_id,
        ))

        conn.commit()

        return {
            "success": True,
            "message": "Feedback updated successfully"
        }

    except Exception as e:
        print("❌ UPDATE FEEDBACK ERROR:", e)
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        safe_close(conn, cursor)


# ======================================================
# DELETE FEEDBACK
# Admin xoá feedback
# ======================================================
@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            DELETE FROM feedback
            WHERE feedback_id = %s
        """, (feedback_id,))

        conn.commit()

        return {
            "success": True,
            "message": "Feedback deleted successfully"
        }

    except Exception as e:
        print("❌ DELETE FEEDBACK ERROR:", e)
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        safe_close(conn, cursor)