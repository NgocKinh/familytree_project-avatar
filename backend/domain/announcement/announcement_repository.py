from typing import List, Optional, Dict, Any

from backend.db import get_connection
from backend.domain.announcement.announcement_schema import (
    AnnouncementCreate
)


# ======================================================
# LIST ANNOUNCEMENTS
# ======================================================

def list_announcements() -> List[Dict[str, Any]]:

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM announcements
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


# ======================================================
# GET ANNOUNCEMENT BY ID
# ======================================================

def get_announcement_by_id(
    announcement_id: int
) -> Optional[Dict[str, Any]]:

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM announcements
        WHERE id = %s
    """, (announcement_id,))

    item = cursor.fetchone()

    cursor.close()
    conn.close()

    return item


# ======================================================
# CREATE ANNOUNCEMENT
# ======================================================

def create_announcement(
    data: AnnouncementCreate
) -> Dict[str, Any]:

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    payload = data.model_dump()

    cursor.execute("""
        INSERT INTO announcements (
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
            is_active
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """, (
        payload["title"],
        payload["description"],
        payload["event_type"],
        payload["calendar_type"],
        payload["solar_date"],
        payload["lunar_day"],
        payload["lunar_month"],
        payload["lunar_year"],
        payload["repeat_type"],
        payload["person_id"],
        payload["is_active"],
    ))

    conn.commit()

    new_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return get_announcement_by_id(new_id)


# ======================================================
# DELETE ANNOUNCEMENT
# ======================================================

def delete_announcement(
    announcement_id: int
) -> bool:

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM announcements
        WHERE id = %s
    """, (announcement_id,))

    deleted = cursor.rowcount > 0

    conn.commit()

    cursor.close()
    conn.close()

    return deleted