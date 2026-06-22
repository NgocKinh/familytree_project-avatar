"""
API: Announcement (v4.1-CLEAN-NAME-ORDER)
-----------------------------------------
- Tự động nhận diện giỗ âm/dương
- Ưu tiên anniversary_death (dd/mm âm lịch)
- Nếu rỗng → dùng death_date (dương lịch)
- Thông báo hôm nay + 7 ngày tới
- Format đẹp (Style B)
- Ultra Safe: try/except + safe_close
"""

from fastapi import APIRouter
from backend.db import get_connection
from lunarcalendar import Converter, Lunar
from datetime import date, timedelta
from backend.domain.announcement.lunar_utils import get_can_chi_year
router = APIRouter()


# ------------------------------------------------------------
# Safe close
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# Convert dd/mm âm lịch → ngày dương lịch năm nay
# ------------------------------------------------------------
def lunar_to_solar_this_year(lunar_ddmm: str):
    try:
        d, m = lunar_ddmm.split("/")
        year_now = date.today().year
        lunar_obj = Lunar(year_now, int(m), int(d), False)
        solar = Converter.Lunar2Solar(lunar_obj)
        return date(solar.year, solar.month, solar.day)
    except Exception as e:
        print("⚠️ Lỗi âm→dương:", e)
        return None


# ------------------------------------------------------------
# Build message Style B
# ------------------------------------------------------------
def build_message(name, lunar_str, solar_date):
    solar_str = solar_date.strftime("%d/%m/%Y")
    return (
        f"🕯️ Hôm nay là đám giỗ của {name}\n"
        f"→ Âm lịch: {lunar_str}\n"
        f"→ Dương lịch năm nay: {solar_str}"
    )
def build_full_name(row):
    return (
        f"{row['sur_name']} "
        f"{row['last_name']} "
        f"{row['middle_name']} "
        f"{row['first_name']}"
    ).strip()

# ------------------------------------------------------------
# Hôm nay
# ------------------------------------------------------------
@router.get("/today")
def announcement_today():

    conn = None
    cursor = None

    try:
        today = date.today()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ⭐ FIX THỨ TỰ TÊN – CHUẨN CẤU TRÚC PROJECT
        cursor.execute("""
            SELECT 
                person_id,
                sur_name,
                last_name,
                middle_name,
                first_name,
                birth_date,
                anniversary_death,
                anniversary_type,
                death_date
            FROM persons
            WHERE delete_status = 0
        """)

        rows = cursor.fetchall()
        result = []

        for row in rows:

            full_name = f"{row['sur_name']} {row['last_name']} {row['middle_name']} {row['first_name']}".strip()
            ann = row["anniversary_death"]
            ann_type = (row.get("anniversary_type") or "lunar").strip().lower()

            # ---------------------------
            # Trường hợp có ngày giỗ riêng
            # ---------------------------
            if ann:

                # GIỖ ÂM
                if ann_type == "lunar":
                    solar = lunar_to_solar_this_year(ann)

                    if solar and solar == today:
                        result.append({
                            "type": "gio",
                            "icon": "🕯️",
                            "title": f"Giỗ {full_name}",
                            "date": solar.strftime("%d/%m/%Y"),
                            "lunar": ann,
                            "lunar_year_name": get_can_chi_year(today.year),
                            "calendar_type": "lunar",
                        })

                # GIỖ DƯƠNG
                elif ann_type == "solar":

                    try:
                        d, m = ann.split("/")
                        solar_this_year = date(today.year, int(m), int(d))

                        if solar_this_year == today:

                            lunar_today = Converter.Solar2Lunar(solar_this_year)
                            lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

                            result.append({
                                "type": "gio",
                                "icon": "🕯️",
                                "title": f"Giỗ {full_name}",
                                "date": solar_this_year.strftime("%d/%m/%Y"),
                                "lunar": lunar_str,
                                "lunar_year_name": get_can_chi_year(today.year),
                                "calendar_type": "solar",
                            })

                    except Exception as e:
                        print("❌ SOLAR ERROR:", full_name, e)

            # ---------------------------
            # Không có ngày giỗ riêng → fallback ngày mất dương lịch
            # ---------------------------
            else:
                dd = row["death_date"]
                if dd:
                    solar_this_year = date(today.year, dd.month, dd.day)

                    if solar_this_year == today:
                        lunar_today = Converter.Solar2Lunar(solar_this_year)
                        lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

                        result.append({
                            "type": "gio",
                            "icon": "🕯️",
                            "title": f"Giỗ {full_name}",
                            "date": solar_this_year.strftime("%d/%m/%Y"),
                            "lunar": lunar_str,
                            "lunar_year_name": get_can_chi_year(today.year),
                            "calendar_type": "solar",
                        })
            # ------------------------------------------------
            # SINH NHẬT DƯƠNG LỊCH
            # ------------------------------------------------
            bd = row.get("birth_date")

            if bd and not row.get("death_date"):
                birthday_this_year = date(
                    today.year,
                    bd.month,
                    bd.day
                )

                if birthday_this_year == today:

                    age = today.year - bd.year

                    result.append({
                        "type": "birthday",
                        "icon": "🎂",
                        "title": f"Sinh nhật {full_name}",
                        "date": birthday_this_year.strftime("%d/%m/%Y"),
                        "age": age,
                        "calendar_type": "solar",
                    })
        # ------------------------------------------------------------
        # KỶ NIỆM NGÀY CƯỚI HÔM NAY
        # ------------------------------------------------------------
        cursor.execute("""
            SELECT
                m.id,
                m.start_date,
                pa.sur_name AS a_sur_name,
                pa.last_name AS a_last_name,
                pa.middle_name AS a_middle_name,
                pa.first_name AS a_first_name,
                pb.sur_name AS b_sur_name,
                pb.last_name AS b_last_name,
                pb.middle_name AS b_middle_name,
                pb.first_name AS b_first_name
            FROM marriages m
            JOIN persons pa ON pa.person_id = m.spouse_a_id
            JOIN persons pb ON pb.person_id = m.spouse_b_id
            WHERE m.start_date IS NOT NULL
                AND m.status = 'married'
        """)

        marriage_rows = cursor.fetchall()

        for m in marriage_rows:
            start_date = m["start_date"]
            wedding_this_year = date(today.year, start_date.month, start_date.day)

            if wedding_this_year == today:
                spouse_a_name = f"{m['a_sur_name']} {m['a_last_name']} {m['a_middle_name']} {m['a_first_name']}".strip()
                spouse_b_name = f"{m['b_sur_name']} {m['b_last_name']} {m['b_middle_name']} {m['b_first_name']}".strip()

                years = today.year - start_date.year

                result.append({
                    "type": "wedding",
                    "icon": "💍",
                    "title": f"Kỷ niệm ngày cưới {spouse_a_name} & {spouse_b_name}",
                    "date": wedding_this_year.strftime("%d/%m/%Y"),
                    "years": years,
                    "calendar_type": "solar",
                })

        lunar_today = Converter.Solar2Lunar(today)
        lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

        return {
            "date": today.strftime("%d/%m/%Y"),
            "lunar": lunar_str,
            "lunar_year_name": get_can_chi_year(today.year),
            "announcements": result
        }

    except Exception as e:
        print("❌ ERROR TODAY:", e)
        return {"error": str(e)}

    finally:
        safe_close(conn, cursor)

# ------------------------------------------------------------
# Sắp tới 7 ngày
# ------------------------------------------------------------
@router.get("/upcoming")
def announcement_upcoming():

    conn = None
    cursor = None

    try:
        today = date.today()
        next_7 = today + timedelta(days=7)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DATABASE() AS db_name")
        # ⭐ FIX THỨ TỰ TÊN – CHUẨN CẤU TRÚC PROJECT
        cursor.execute("""
            SELECT 
                person_id,
                sur_name,
                last_name,
                middle_name,
                first_name,
                birth_date,
                anniversary_death,
                anniversary_type,
                death_date
            FROM persons
            WHERE delete_status = 0
        """)

        rows = cursor.fetchall()
        result = []

        for row in rows:

            full_name = f"{row['sur_name']} {row['last_name']} {row['middle_name']} {row['first_name']}".strip()
            ann = row["anniversary_death"]
            ann_type = (row.get("anniversary_type") or "lunar").strip().lower()
            if ann:

                # GIỖ ÂM
                if ann_type == "lunar":
                    solar = lunar_to_solar_this_year(ann)

                    if solar and today < solar <= next_7:
                        result.append({
                            "type": "gio",
                            "icon": "🕯️",
                            "title": f"Giỗ {full_name}",
                            "date": solar.strftime("%d/%m/%Y"),
                            "lunar": ann,
                            "lunar_year_name": get_can_chi_year(today.year),
                            "calendar_type": "lunar",
                        })

                # GIỖ DƯƠNG
                elif ann_type == "solar":
                    d, m = ann.split("/")
                    solar_this_year = date(today.year, int(m), int(d))

                    if today < solar_this_year <= next_7:
                        lunar_today = Converter.Solar2Lunar(solar_this_year)
                        lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

                        result.append({
                            "type": "gio",
                            "icon": "🕯️",
                            "title": f"Giỗ {full_name}",
                            "date": solar_this_year.strftime("%d/%m/%Y"),
                            "lunar": lunar_str,
                            "lunar_year_name": get_can_chi_year(today.year),
                            "calendar_type": "solar",
                        })

            # ---------------------------
            # GIỖ DƯƠNG
            # ---------------------------
            else:
                dd = row["death_date"]
                if dd:
                    solar_this_year = date(today.year, dd.month, dd.day)
                    if today < solar_this_year <= next_7:

                        lunar_today = Converter.Solar2Lunar(solar_this_year)
                        lunar_str = f"{str(lunar_today.day).zfill(2)}/{str(lunar_today.month).zfill(2)}"

                        result.append({
                            "type": "gio",
                            "icon": "🕯️",
                            "title": f"Giỗ {full_name}",
                            "date": solar_this_year.strftime("%d/%m/%Y"),
                            "lunar": lunar_str,
                            "lunar_year_name": get_can_chi_year(today.year),
                            "calendar_type": "solar",
                        })
            # ------------------------------------------------
            # SINH NHẬT SẮP TỚI
            # ------------------------------------------------
            bd = row.get("birth_date")

            if bd and not row.get("death_date"):

                birthday_this_year = date(
                    today.year,
                    bd.month,
                    bd.day
                )

                if today < birthday_this_year <= next_7:

                    age = today.year - bd.year

                    result.append({
                        "type": "birthday",
                        "icon": "🎂",
                        "title": f"Sinh nhật {full_name}",
                        "date": birthday_this_year.strftime("%d/%m/%Y"),
                        "age": age,
                        "calendar_type": "solar",
                    })
        # ------------------------------------------------------------
        # KỶ NIỆM NGÀY CƯỚI SẮP TỚI
        # ------------------------------------------------------------
        cursor.execute("""
            SELECT
                m.id,
                m.start_date,
                pa.sur_name AS a_sur_name,
                pa.last_name AS a_last_name,
                pa.middle_name AS a_middle_name,
                pa.first_name AS a_first_name,
                pb.sur_name AS b_sur_name,
                pb.last_name AS b_last_name,
                pb.middle_name AS b_middle_name,
                pb.first_name AS b_first_name
            FROM marriages m
            JOIN persons pa ON pa.person_id = m.spouse_a_id
            JOIN persons pb ON pb.person_id = m.spouse_b_id
            WHERE m.start_date IS NOT NULL
                AND m.status = 'married'
        """)

        marriage_rows = cursor.fetchall()

        for m in marriage_rows:
            start_date = m["start_date"]
            wedding_this_year = date(today.year, start_date.month, start_date.day)

            if today < wedding_this_year <= next_7:
                spouse_a_name = f"{m['a_sur_name']} {m['a_last_name']} {m['a_middle_name']} {m['a_first_name']}".strip()
                spouse_b_name = f"{m['b_sur_name']} {m['b_last_name']} {m['b_middle_name']} {m['b_first_name']}".strip()

                years = today.year - start_date.year

                result.append({
                    "type": "wedding",
                    "icon": "💍",
                    "title": f"Kỷ niệm ngày cưới {spouse_a_name} & {spouse_b_name}",
                    "date": wedding_this_year.strftime("%d/%m/%Y"),
                    "years": years,
                    "calendar_type": "solar",
                })
                    
        return {
            "range_days": 7,
            "announcements": result
        }

    except Exception as e:
        print("❌ ERROR UPCOMING:", e)
        return {"error": str(e)}

    finally:
        safe_close(conn, cursor)

# ------------------------------------------------------------
# Thông báo chung đang active
# ------------------------------------------------------------
@router.get("/list")
def announcement_list():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                title,
                description,
                event_type,
                calendar_type,
                solar_date,
                lunar_day,
                lunar_month,
                lunar_year,
                repeat_type,
                person_id,
                is_active,
                created_at
            FROM announcements
            WHERE is_active = 1
            ORDER BY created_at DESC
        """)

        rows = cursor.fetchall()

        return {
            "success": True,
            "data": rows
        }

    except Exception as e:
        print("❌ ERROR ANNOUNCEMENT LIST:", e)
        return {
            "success": False,
            "error": str(e),
            "data": []
        }

    finally:
        safe_close(conn, cursor)
