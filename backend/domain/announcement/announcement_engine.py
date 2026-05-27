from datetime import date
from typing import List, Dict, Any

from backend.domain.announcement.announcement_repository import (
    list_announcements
)


# ======================================================
# GET TODAY ANNOUNCEMENTS
# ======================================================

def get_today_announcements() -> List[Dict[str, Any]]:

    today = str(date.today())

    announcements = list_announcements()

    results = []

    for item in announcements:

        if not item["is_active"]:
            continue

        if item["calendar_type"] == "solar":

            if item["solar_date"] == today:
                results.append(item)

    return results


# ======================================================
# GET UPCOMING ANNOUNCEMENTS
# ======================================================

def get_upcoming_announcements() -> List[Dict[str, Any]]:

    announcements = list_announcements()

    results = []

    for item in announcements:

        if not item["is_active"]:
            continue

        results.append(item)

    return results