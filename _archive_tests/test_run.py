from datetime import datetime

from backend.db import SessionLocal
from backend.services.marriage_service import create_marriage
from backend.models.person_model import Person
from backend.models.marriage_model import Marriage


# ===== Fake request object (PHẢI match đúng service contract) =====
class Fake:
    def __init__(self, a, b):
        self.person1_id = a
        self.person2_id = b
        self.start_date = datetime.now()


def run():
    db = SessionLocal()

    print("DB URL:", db.bind.url)

    try:
        # ==========================================================
        # 🧱 STEP 1: CLEAN STATE (tránh data cũ gây nhiễu)
        # ==========================================================
        print("\n=== Cleaning old test data ===")

        db.query(Marriage).delete()
        db.query(Person).delete()
        db.commit()

        # ==========================================================
        # 🧱 STEP 2: SETUP TEST DATA
        # ==========================================================
        print("\n=== Setup test data ===")

        p1 = Person(name="User_A")
        p2 = Person(name="User_B")
        p3 = Person(name="User_C")

        db.add_all([p1, p2, p3])
        db.commit()

        db.refresh(p1)
        db.refresh(p2)
        db.refresh(p3)

        print(f"Created users: {p1.id}, {p2.id}, {p3.id}")

        # ==========================================================
        # 🧪 TEST 1: First marriage (PHẢI SUCCESS)
        # ==========================================================
        print("\n=== Test 1: First marriage ===")

        try:
            create_marriage(db, Fake(p1.id, p2.id))
            print("✅ PASS: First marriage created")
        except Exception as e:
            print("❌ FAIL:", e)
            return

        # Debug check
        count = db.query(Marriage).count()
        print("Marriage count after test 1:", count)

        if count != 1:
            print("❌ BUG: Expected 1 marriage")
            return

        # ==========================================================
        # 🧪 TEST 2: Second marriage (PHẢI FAIL)
        # ==========================================================
        print("\n=== Test 2: Second marriage (should fail) ===")

        try:
            create_marriage(db, Fake(p1.id, p3.id))
            print("❌ FAIL: Allowed second active marriage")
        except Exception as e:
            print("✅ PASS:", e)

        # ==========================================================
        # 🧪 TEST 3: Reverse order (edge case)
        # ==========================================================
        print("\n=== Test 3: Reverse order (should fail) ===")

        try:
            create_marriage(db, Fake(p2.id, p1.id))
            print("❌ FAIL: Allowed duplicate reverse marriage")
        except Exception as e:
            print("✅ PASS:", e)

        # ==========================================================
        # 🧪 FINAL STATE CHECK
        # ==========================================================
        print("\n=== Final DB State ===")

        marriages = db.query(Marriage).all()
        print(f"Total marriages: {len(marriages)}")

        for m in marriages:
            print(
                f"Marriage: {m.person1_id} - {m.person2_id}, active={m.is_active}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    run()