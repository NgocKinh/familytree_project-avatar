import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")
# =====================================
# 🔵 MYSQL CONNECTION
# =====================================

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "familytreedb"),
        charset="utf8mb4"
    )

# =====================================
# 🔵 GET PARENTS FROM MYSQL
# =====================================

def get_parents(person_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT parent_id, type
        FROM parent_child
        WHERE child_id = %s
        """,
        (person_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    parents = []

    for row in rows:
        parents.append(
            (
                row["parent_id"],
                row["type"]
            )
        )

    return parents

# =====================================
# 🔵 GET SIBLINGS FROM MYSQL
# =====================================

def get_siblings(person_id):

    siblings = set()

    # lấy cha mẹ thật từ MySQL
    parents = get_parents(person_id)

    # duyệt từng cha/mẹ
    for parent_id, role in parents:

        # lấy tất cả con của cha/mẹ đó
        children = get_children(parent_id)
        
        # loại chính mình ra
        for child_id in children:
            if child_id != person_id:
                siblings.add(child_id)

    return list(siblings)

# =====================================
# 🔵 GET SPOUSE FROM MYSQL
# =====================================

def get_spouse(person_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT spouse_a_id, spouse_b_id
        FROM marriages
        WHERE spouse_a_id = %s
           OR spouse_b_id = %s
        LIMIT 1
        """,
        (person_id, person_id)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    if row["spouse_a_id"] == person_id:
        return row["spouse_b_id"]

    return row["spouse_a_id"]

def get_spouses(person_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT spouse_a_id, spouse_b_id
        FROM marriages
        WHERE spouse_a_id = %s
           OR spouse_b_id = %s
        """,
        (person_id, person_id)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    spouses = []

    for row in rows:
        if row["spouse_a_id"] == person_id:
            spouses.append(row["spouse_b_id"])
        else:
            spouses.append(row["spouse_a_id"])

    return spouses   

# =====================================
# 🔵 GET CHILDREN FROM MYSQL
# =====================================

def get_children(parent_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT child_id
        FROM parent_child
        WHERE parent_id = %s
        """,
        (parent_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    children = []

    for row in rows:
        children.append(row["child_id"])

    return children

# =====================================
# 🔵 GET BIRTH YEAR FROM MYSQL
# =====================================

def get_birth(person_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT birth_date
        FROM persons
        WHERE person_id = %s
        """,
        (person_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    birth_date = row["birth_date"]

    if not birth_date:
        return None

    return birth_date.year
# =====================================
# 🔵 GET BIRTH ORDER FROM MYSQL
# =====================================

def get_birth_order(person_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT birth_order
        FROM persons
        WHERE person_id = %s
        """,
        (person_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return row["birth_order"]
# =====================================
# 🔵 GET GENDER FROM MYSQL
# =====================================

def get_gender(person_id):

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT gender
        FROM persons
        WHERE person_id = %s
        """,
        (person_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return row["gender"]           