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
        print("DEBUG DB:", cursor.fetchone())
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
            print("DEBUG ANN:", row["person_id"], ann, ann_type)
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

        return {
            "range_days": 7,
            "announcements": result
        }

    except Exception as e:
        print("❌ ERROR UPCOMING:", e)
        return {"error": str(e)}

    finally:
        safe_close(conn, cursor)
