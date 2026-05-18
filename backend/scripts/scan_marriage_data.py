from backend.db import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("=== QUERY 1: SELF RELATIONSHIP ===")
q1 = db.execute(text("""
SELECT * FROM marriages
WHERE spouse_a_id = spouse_b_id;
"""))
rows1 = q1.fetchall()
print("Count:", len(rows1))


print("\n=== QUERY 2: DUPLICATE ACTIVE MARRIAGE ===")
q2 = db.execute(text("""
SELECT spouse_a_id, spouse_b_id, COUNT(*)
FROM marriages
WHERE status IN ('married', 'cohabiting')
GROUP BY spouse_a_id, spouse_b_id
HAVING COUNT(*) > 1;
"""))
rows2 = q2.fetchall()
print("Count:", len(rows2))


print("\n=== QUERY 3: MULTIPLE ACTIVE PER PERSON ===")
q3 = db.execute(text("""
SELECT person_id, COUNT(*)
FROM (
    SELECT spouse_a_id AS person_id FROM marriages WHERE status IN ('married', 'cohabiting')
    UNION ALL
    SELECT spouse_b_id AS person_id FROM marriages WHERE status IN ('married', 'cohabiting')
) t
GROUP BY person_id
HAVING COUNT(*) > 1;
"""))
rows3 = q3.fetchall()

print("Count:", len(rows3))

for row in rows3:
    print("Person ID:", row[0], "| Active marriages:", row[1])

# 🔥 in chi tiết marriages của người đó
for row in rows3:
    person_id = row[0]
    print(f"\n--- Details for person {person_id} ---")

    detail = db.execute(text("""
    SELECT id, spouse_a_id, spouse_b_id, status
    FROM marriages
    WHERE status IN ('married', 'cohabiting')
    AND (spouse_a_id = :pid OR spouse_b_id = :pid)
    """), {"pid": person_id})

    for d in detail.fetchall():
        print(d)
    print("\n=== FIXING INVALID DATA ===")

    # 👉 disable record cũ (id = 40)
    db.execute(text("""
    UPDATE marriages
    SET status = 'divorced'
    WHERE id = 40
    """))

    db.commit()

    print("Fixed: set marriage id=40 to 'divorced'")
    print("\n=== RE-CHECK AFTER FIX ===")

    recheck = db.execute(text("""
    SELECT person_id, COUNT(*)
    FROM (
        SELECT spouse_a_id AS person_id FROM marriages WHERE status IN ('married', 'cohabiting')
        UNION ALL
        SELECT spouse_b_id AS person_id FROM marriages WHERE status IN ('married', 'cohabiting')
    ) t
    GROUP BY person_id
    HAVING COUNT(*) > 1;
    """))

    rows = recheck.fetchall()
    print("Remaining issues:", len(rows))
db.close()