# ==========================================================
# tree_api.py v6 – GENEALOGY STABLE
# ==========================================================

from flask import Blueprint, jsonify
from backend.db import get_connection
import os

tree_bp = Blueprint("tree_bp", __name__)

AVATAR_PATH = os.path.join("backend", "static", "avatars")
# ==========================================================
# ✅ [ADDED]: fallback chuẩn cho person
# ==========================================================
def safe_person(p):
    if not p:
        return {
            "person_id": None,
            "name": "Không rõ",
            "gender": None,
            "birth_year": None,
            "death_year": None,
            "avatar": "/static/avatars/default_other.png"
        }
    return p

# ----------------------------------------------------------
# Avatar
# ----------------------------------------------------------

def resolve_avatar(p):
    if not p:
        return None

    pid = p["person_id"]
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
            person_id AS person_id,
            full_name_vn AS name,
            gender,
            YEAR(birth_date) AS birth_year,
            YEAR(death_date) AS death_year
        FROM person
        WHERE person_id = %s
        AND delete_status = 0
    """, (pid,))

    p = cur.fetchone()

    cur.close()
    conn.close()

    if p:
        p["avatar"] = resolve_avatar(p)

    return p


# ----------------------------------------------------------
# GET SPOUSE (LATEST MARRIAGE)
# ----------------------------------------------------------

def get_spouse(pid):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            m.status,
            person_id AS person_id,
            p.full_name_vn AS name,
            p.gender,
            YEAR(p.birth_date) AS birth_year,
            YEAR(p.death_date) AS death_year
        FROM marriage m
        JOIN person p
          ON (p.person_id = m.spouse_a_id OR p.person_id = m.spouse_b_id)
        WHERE (m.spouse_a_id = %s OR m.spouse_b_id = %s)
        AND p.person_id != %s
        ORDER BY m.start_date DESC
        LIMIT 1
    """, (pid, pid, pid))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None, None

    spouse = {
        "person_id": row["person_id"],
        "name": row["name"],
        "gender": row["gender"],
        "birth_year": row["birth_year"],
        "death_year": row["death_year"],
        "avatar": resolve_avatar(row)
    }

    return spouse, row["status"]


# ----------------------------------------------------------
# GET PARENTS
# ----------------------------------------------------------

def get_parents(pid):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            person_id AS person_id,
            p.full_name_vn AS name,
            p.gender,
            YEAR(p.birth_date) AS birth_year,
            YEAR(p.death_date) AS death_year
        FROM parent_child pc
        JOIN person p ON p.person_id = pc.parent_id
        WHERE pc.child_id = %s
        AND pc.type IN ('father','mother')
    """, (pid,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    for r in rows:
        r["avatar"] = resolve_avatar(r)

    return rows


# ----------------------------------------------------------
# GET CHILDREN (BLOOD)
# ----------------------------------------------------------

def get_children(center_id, spouse_id):

    if not spouse_id:
        return []

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            person_id AS person_id,
            full_name_vn AS name,
            gender,
            YEAR(birth_date) AS birth_year,
            YEAR(death_date) AS death_year
        FROM person
        WHERE blood_code = CONCAT(%s,'|',%s)
           OR blood_code = CONCAT(%s,'|',%s)
    """, (center_id, spouse_id, spouse_id, center_id))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    for r in rows:
        r["avatar"] = resolve_avatar(r)

    return rows


# ----------------------------------------------------------
# MAIN API
# ----------------------------------------------------------

@tree_bp.route("/family/<int:pid>")
def get_family(pid):

    center = get_person(pid)

    if not center:
        return jsonify({"error": "not_found"}), 404

    spouse, status = get_spouse(pid)

    # ----------------------------------
    # xác định người nam / nữ
    # ----------------------------------

    male = None
    female = None

    if center["gender"] == "male":
        male = center
        female = spouse
    elif center["gender"] == "female":
        female = center
        male = spouse

    father_parents = []
    mother_parents = []

    if male:
        father_parents = get_parents(male["person_id"])

    if female:
        mother_parents = get_parents(female["person_id"])

    # ----------------------------------
    # children
    # ----------------------------------

    spouse_id = spouse["person_id"] if spouse else None

    children_common = get_children(center["person_id"], spouse_id)

    # ----------------------------------
    # response
    # ----------------------------------

    return jsonify({

        "center": safe_person(center),
        "spouse": safe_person(spouse),
        "marriage_status": status,

        "father_parents": father_parents,
        "mother_parents": mother_parents,

        "children_common": children_common

    })