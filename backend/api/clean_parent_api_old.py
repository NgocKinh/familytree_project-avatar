from fastapi import APIRouter, HTTPException
from backend.db import get_connection

router = APIRouter()


@router.post("/api/clean/parent")
def add_parent(data: dict):
    print("🔥 DATA RECEIVED:", data)
    child_id = data.get("child_id")
    parent_id = data.get("parent_id")
    relation_type = data.get("type")        # FATHER | MOTHER
    marriage_id = data.get("marriage_id")

    # -------------------------
    # Validate input cơ bản
    # -------------------------
    if not child_id or not parent_id or not relation_type:
        raise HTTPException(status_code=400, detail="Thiếu dữ liệu bắt buộc")

    if relation_type not in ("FATHER", "MOTHER"):
        raise HTTPException(status_code=400, detail="Loại quan hệ không hợp lệ")

    if child_id == parent_id:
        raise HTTPException(status_code=400, detail="Cha/Mẹ và Con không thể là cùng một người")

    conn = None
    cur = None

    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        # -------------------------
        # Kiểm tra child tồn tại
        # -------------------------
        cur.execute(
            "SELECT person_id FROM person WHERE person_id=%s AND delete_status=0",
            (child_id,)
        )

        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Không tìm thấy người con")

        # -------------------------
        # Kiểm tra parent tồn tại + giới tính
        # -------------------------
        cur.execute(
            "SELECT person_id, gender FROM person WHERE person_id=%s AND delete_status=0",
            (parent_id,)
        )

        parent = cur.fetchone()

        if not parent:
            raise HTTPException(status_code=404, detail="Không tìm thấy cha/mẹ")

        if relation_type == "FATHER" and parent["gender"] != "male":
            raise HTTPException(status_code=400, detail="Giới tính không phù hợp (FATHER phải là male)")

        if relation_type == "MOTHER" and parent["gender"] != "female":
            raise HTTPException(status_code=400, detail="Giới tính không phù hợp (MOTHER phải là female)")

        # -------------------------
        # Kiểm tra đã có FATHER / MOTHER chưa
        # -------------------------
        cur.execute("""
            SELECT id FROM parent_child
            WHERE child_id=%s AND type=%s
        """, (child_id, relation_type))

        if cur.fetchone():
            raise HTTPException(status_code=400, detail=f"Người này đã có {relation_type}")

        # -------------------------
        # (OPTIONAL) Kiểm tra marriage nếu có
        # -------------------------
        if marriage_id:
            cur.execute(
                "SELECT id FROM marriages WHERE id=%s",
                (marriage_id,)
            )

            if not cur.fetchone():
                raise HTTPException(status_code=400, detail="Marriage không tồn tại")

        # -------------------------
        # INSERT parent_child
        # -------------------------
        cur.execute("""
            INSERT INTO parent_child (parent_id, child_id, type)
            VALUES (%s, %s, %s)
        """, (parent_id, child_id, relation_type))

        conn.commit()

        return {
            "message": "Đã thêm cha/mẹ thành công",
            "child_id": child_id,
            "parent_id": parent_id,
            "type": relation_type,
            "marriage_id": marriage_id
        }

    except HTTPException:
        raise

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()

        if conn and conn.is_connected():   
            conn.close()