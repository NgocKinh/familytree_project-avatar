# ==========================================================
# FastAPI version of tree_api (migrated from Flask)
# ==========================================================

from fastapi import APIRouter, HTTPException
from backend.db import get_connection  # chỉnh lại nếu path khác
import os

router = APIRouter(prefix="/api/tree", tags=["Tree"])

ENABLE_SOCIAL_CHILDREN = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_PATH = os.path.join(BASE_DIR, "static", "avatars")


# ----------------------------------------------------------
# Avatar engine
# ----------------------------------------------------------
def resolve_avatar(p):
    if not p:
        return None
    pid = p["id"]
    gender = p.get("gender", "other")

    png = os.path.join(AVATAR_PATH, f"{pid}.png")
    jpg = os.path.join(AVATAR_PATH, f"{pid}.jpg")

    if os.path.exists(png):
        return f"/static/avatars/{pid}.png"
    if os.path.exists(jpg):
        return f"/static/avatars/{pid}.jpg"

    if gender == "male":
        return "/static/avatars/default_male.png"
    if gender == "female":
        return "/static/avatars/default_female.png"
    return "/static/avatars/default_other.png"


# ----------------------------------------------------------
# GET PERSON
# ----------------------------------------------------------
def get_person(pid):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            person_id AS id,
            full_name_vn AS name,
            gender,
            YEAR(birth_date) AS birth_year,
            YEAR(death_date) AS death_year
        FROM person
        WHERE person_id = %s AND delete_status = 0
    """, (pid,))

    p = cur.fetchone()
    cur.close()
    conn.close()

    if p:
        p["avatar"] = resolve_avatar(p)
    return p


# ----------------------------------------------------------
# MAIN API
# ----------------------------------------------------------
@router.get("/family/{pid}")
def get_family(pid: int):
    center = get_person(pid)

    if not center:
        raise HTTPException(status_code=404, detail="not_found")

    # ----------------------------------------------------------
    # GET SPOUSE
    # ----------------------------------------------------------
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            m.status,
            CASE
                WHEN m.spouse_a_id = %s THEN m.spouse_b_id
                ELSE m.spouse_a_id
            END AS spouse_id
        FROM marriage m
        WHERE m.spouse_a_id = %s OR m.spouse_b_id = %s
        ORDER BY
            CASE m.status
                WHEN 'married' THEN 1
                WHEN 'cohabitation' THEN 2
                WHEN 'separated' THEN 3
                WHEN 'divorced' THEN 4
                ELSE 5
            END
        LIMIT 1
    """, (pid, pid, pid))

    row = cur.fetchone()

    spouse = None
    marriage_status = None

    if row:
        spouse = get_person(row["spouse_id"])
        marriage_status = row["status"]

    cur.close()
    conn.close()

    return {
        "center": center,
        "spouse": spouse,
        "marriage_status": marriage_status,
        "father_parents": [],
        "mother_parents": [],
        "children_common": [],
        "children_father_separate": [],
        "children_mother_separate": [],
        "children_social": [],
    }