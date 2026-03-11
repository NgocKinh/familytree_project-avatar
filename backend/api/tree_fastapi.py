from fastapi import APIRouter, HTTPException
from backend.db import get_connection
import os
import time

router = APIRouter(tags=["Tree"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AVATAR_PATH = os.path.join(BASE_DIR, "static", "avatars")

# ----------------------------------------------------------
# SIMPLE MEMORY CACHE (tree cực nhanh)
# ----------------------------------------------------------

TREE_CACHE = {}
CACHE_TTL = 30   # seconds


# ----------------------------------------------------------
# Avatar
# ----------------------------------------------------------

def resolve_avatar(pid, gender):

    jpg = os.path.join(AVATAR_PATH, f"{pid}.jpg")

    if os.path.exists(jpg):
        return f"/static/avatars/{pid}.jpg"

    if gender == "male":
        return "/static/avatars/default_male.png"

    if gender == "female":
        return "/static/avatars/default_female.png"

    return "/static/avatars/default_other.png"


# ----------------------------------------------------------
# Helper
# ----------------------------------------------------------

def build_person(row):

    if not row:
        return None

    p = dict(row)

    p["avatar"] = resolve_avatar(p["person_id"], p["gender"])

    return p


# ----------------------------------------------------------
# MAIN API
# ----------------------------------------------------------

@router.get("/family/{pid}")
def get_family(pid: int):

    # ----------------------------------------------------------
    # CACHE
    # ----------------------------------------------------------

    now = time.time()

    cached = TREE_CACHE.get(pid)

    if cached and now - cached["time"] < CACHE_TTL:
        return cached["data"]

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ----------------------------------------------------------
    # CENTER
    # ----------------------------------------------------------

    cur.execute(
        """
        SELECT
            person_id AS person_id,
            full_name_vn AS name,
            gender,
            YEAR(birth_date) AS birth_year,
            YEAR(death_date) AS death_year
        FROM person
        WHERE person_id = %s
        """,
        (pid,),
    )

    center = build_person(cur.fetchone())

    if not center:
        raise HTTPException(status_code=404)

    # ----------------------------------------------------------
    # SPOUSE
    # ----------------------------------------------------------

    cur.execute(
        """
        SELECT
            CASE
                WHEN spouse_a_id = %s THEN spouse_b_id
                ELSE spouse_a_id
            END AS spouse_id,
            status
        FROM marriage
        WHERE spouse_a_id = %s OR spouse_b_id = %s
        ORDER BY
            CASE status
                WHEN 'married' THEN 1
                WHEN 'cohabitation' THEN 2
                WHEN 'separated' THEN 3
                WHEN 'divorced' THEN 4
                ELSE 5
            END
        LIMIT 1
        """,
        (pid, pid, pid),
    )

    row = cur.fetchone()

    spouse = None
    marriage_status = None

    if row:

        marriage_status = row["status"]

        cur.execute(
            """
            SELECT
                person_id AS person_id,
                full_name_vn AS name,
                gender,
                YEAR(birth_date) AS birth_year,
                YEAR(death_date) AS death_year
            FROM person
            WHERE person_id = %s
            """,
            (row["spouse_id"],),
        )

        spouse = build_person(cur.fetchone())

    # ----------------------------------------------------------
    # PARENTS
    # ----------------------------------------------------------

    def get_parents(person_id):

        cur.execute(
            """
            SELECT
                person_id AS person_id,
                p.full_name_vn AS name,
                p.gender,
                YEAR(p.birth_date) AS birth_year,
                YEAR(p.death_date) AS death_year
            FROM parent_child pc
            JOIN person p ON pc.parent_id = p.person_id
            WHERE pc.child_id = %s
            """,
            (person_id,),
        )

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
    # ----------------------------------------------------------
    # CHILDREN
    # ----------------------------------------------------------

    children_common = []

    if spouse:

        cur.execute(
            """
            SELECT
                c.person_id AS person_id,
                c.full_name_vn AS name,
                c.gender,
                YEAR(c.birth_date) AS birth_year,
                YEAR(c.death_date) AS death_year
            FROM parent_child pc1
            JOIN parent_child pc2
              ON pc1.child_id = pc2.child_id
            JOIN person c
              ON c.person_id = pc1.child_id
            WHERE pc1.parent_id = %s
              AND pc2.parent_id = %s
            """,
            (center["person_id"], spouse["person_id"]),
        )

        rows = cur.fetchall()

        children_common = sorted(
            [build_person(r) for r in rows],
            key=lambda x: x["birth_year"] or 9999
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

    # ----------------------------------------------------------
    # SAVE CACHE
    # ----------------------------------------------------------

    TREE_CACHE[pid] = {
        "time": now,
        "data": result,
    }

    return result