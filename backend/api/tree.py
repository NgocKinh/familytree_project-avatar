# ==========================================================
# FILE: backend/api/tree.py (FastAPI - CONVERT FROM FLASK)
# GIỮ NGUYÊN LOGIC CŨ (CACHE + SQL + AVATAR)
# ==========================================================

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.db import get_connection

import os
import time

router = APIRouter()

# ==========================================================
# PATH
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_PATH = os.path.join(BASE_DIR, "static", "avatars")

# ==========================================================
# CACHE
# ==========================================================

TREE_CACHE = {}
CACHE_TTL = 30  # seconds

# ==========================================================
# AVATAR
# ==========================================================

def resolve_avatar(pid, gender):

    jpg = os.path.join(AVATAR_PATH, f"{pid}.jpg")

    if os.path.exists(jpg):
        return f"/static/avatars/{pid}.jpg"

    if gender == "male":
        return "/static/avatars/default_male.png"

    if gender == "female":
        return "/static/avatars/default_female.png"

    return "/static/avatars/default_other.png"


# ==========================================================
# HELPER
# ==========================================================

def build_person(row):

    # ✅ [CHANGE 1]: fallback khi không có người
    if not row:
        return {
            "person_id": None,
            "name": "Không rõ",
            "gender": None,
            "birth_year": None,
            "death_year": None,
            "avatar": "/static/avatars/default_other.png"
        }

    p = dict(row)

    p["avatar"] = resolve_avatar(p["person_id"], p.get("gender"))

    return p


# ==========================================================
# MAIN API
# ==========================================================

@router.get("/{pid}")
def get_family(pid: int):
    
    now = time.time()

    # ================= CACHE =================
    cached = TREE_CACHE.get(pid)

    if cached and now - cached["time"] < CACHE_TTL:
        return cached["data"]

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ================= CENTER =================

    cur.execute("""
        SELECT
            person_id,
            full_name_vn AS name,
            sur_name,
            last_name,
            middle_name,
            first_name,
            gender,
            YEAR(birth_date) AS birth_year,
            YEAR(death_date) AS death_year
        FROM persons
        WHERE person_id = %s
    """, (pid,))

    center = build_person(cur.fetchone())

    if not center:
        return JSONResponse({"error": "not_found"}, status_code=404)

    # ================= SPOUSE =================

    # 🔵 STEP 1: tìm tất cả marriages chứa person này
    cur.execute("""
        SELECT
            m.id,
            m.spouse_a_id,
            m.spouse_b_id,
            m.status,
            m.priority

        FROM marriages m

        WHERE
            m.spouse_a_id = %s
            OR m.spouse_b_id = %s
        ORDER BY m.id ASC    
    """, (pid, pid))

    marriage_rows = cur.fetchall()

    spouse = None
    marriage_status = None

    # =========================================================
    # CASE 1: KHÔNG có marriage
    # =========================================================
    if len(marriage_rows) == 0:
        spouse = None

    # =========================================================
    # CASE 2: CHỈ có 1 marriage
    # =========================================================
    elif len(marriage_rows) == 1:

        row = marriage_rows[0]

        marriage_status = row["status"]

        spouse_id = (
            row["spouse_b_id"]
            if row["spouse_a_id"] == pid
            else row["spouse_a_id"]
        )

        cur.execute("""
            SELECT
                person_id,
                full_name_vn AS name,
                sur_name,
                last_name,
                middle_name,
                first_name,
                gender,
                YEAR(birth_date) AS birth_year,
                YEAR(death_date) AS death_year
            FROM persons
            WHERE person_id = %s
        """, (spouse_id,))

        spouse = build_person(cur.fetchone())

    # =========================================================
    # CASE 3: NHIỀU marriages
    # =========================================================
    else:

        best_row = None
        best_priority = -1

        for row in marriage_rows:

            marriage_id = row["id"]

            priority = row["priority"] or 0

            if priority > best_priority:
                best_priority = priority
                best_row = row

        if best_row:

            marriage_status = best_row["status"]

            spouse_id = (
                best_row["spouse_b_id"]
                if best_row["spouse_a_id"] == pid
                else best_row["spouse_a_id"]
            )

            cur.execute("""
                SELECT
                    person_id,
                    full_name_vn AS name,
                    sur_name,
                    last_name,
                    middle_name,
                    first_name,
                    gender,
                    YEAR(birth_date) AS birth_year,
                    YEAR(death_date) AS death_year
                FROM persons
                WHERE person_id = %s
            """, (spouse_id,))

            spouse = build_person(cur.fetchone())

    # 🔵 [ADDED]: Auto widowed nếu 1 trong 2 đã mất
    if spouse and (
        center.get("death_year")
        or spouse.get("death_year")
    ):
        marriage_status = "widowed"
    # ================= PARENTS =================

    def get_parents(person_id):

        cur.execute("""
            SELECT
                p.person_id,
                p.full_name_vn AS name,
                p.sur_name,
                p.last_name,
                p.middle_name,
                p.first_name,
                p.gender,
                YEAR(p.birth_date) AS birth_year,
                YEAR(p.death_date) AS death_year
            FROM parent_child pc
            JOIN persons p ON pc.parent_id = p.person_id
            WHERE pc.child_id = %s
        """, (person_id,))

        rows = cur.fetchall()

        return [build_person(r) for r in rows]

    father_parents = []
    mother_parents = []

    male = None
    female = None

    if center["gender"] == "male":
        male = center
        female = spouse
    else:
        female = center
        male = spouse

    if male:
        father_parents = get_parents(male["person_id"])

    if female:
        mother_parents = get_parents(female["person_id"])

    # ================= CHILDREN =================

    children_common = []

    if spouse:

        cur.execute("""
            SELECT
                c.person_id,
                c.full_name_vn AS name,
                c.sur_name,
                c.last_name,
                c.middle_name,
                c.first_name,
                c.gender,
                YEAR(c.birth_date) AS birth_year,
                YEAR(c.death_date) AS death_year
            FROM parent_child pc1
            JOIN parent_child pc2 ON pc1.child_id = pc2.child_id
            JOIN persons c ON c.person_id = pc1.child_id
            WHERE pc1.parent_id = %s
              AND pc2.parent_id = %s
        """, (center["person_id"], spouse["person_id"]))

        rows = cur.fetchall()

        children_common = sorted(
            [build_person(r) for r in rows],
            key=lambda x: x.get("birth_year") or 9999
        )

    cur.close()
    conn.close()

    result = {
        "center": center,
        "spouse": spouse,
        "marriage_status": marriage_status,
        "father_parents": father_parents,
        "mother_parents": mother_parents,
        "children_common": children_common,
        "children_father_separate": [],
        "children_mother_separate": [],
        "children_social": [],
    }

    # ================= SAVE CACHE =================
    TREE_CACHE[pid] = {
        "time": now,
        "data": result
    }

    return result
