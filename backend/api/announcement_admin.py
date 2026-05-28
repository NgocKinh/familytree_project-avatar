from fastapi import APIRouter, HTTPException

from backend.domain.announcement.announcement_schema import AnnouncementCreate
from backend.domain.announcement.announcement_repository import (
    list_announcements,
    get_announcement_by_id,
    create_announcement,
    update_announcement,
    delete_announcement,
)


router = APIRouter(
    tags=["Announcement Admin"]
)


# ======================================================
# LIST ANNOUNCEMENTS
# ======================================================

@router.get("/list")
def api_list_announcements():
    return {
        "success": True,
        "data": list_announcements()
    }


# ======================================================
# CREATE ANNOUNCEMENT
# ======================================================

@router.post("/create")
def api_create_announcement(data: AnnouncementCreate):
    item = create_announcement(data)

    return {
        "success": True,
        "data": item
    }
# ======================================================
# UPDATE ANNOUNCEMENT
# ======================================================

@router.put("/{announcement_id}")
def api_update_announcement(
    announcement_id: int,
    data: AnnouncementCreate
):

    item = update_announcement(
        announcement_id,
        data
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found"
        )

    return {
        "success": True,
        "data": item
    }

# ======================================================
# GET ANNOUNCEMENT DETAIL
# ======================================================

@router.get("/{announcement_id}")
def api_get_announcement(announcement_id: int):
    item = get_announcement_by_id(announcement_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found"
        )

    return {
        "success": True,
        "data": item
    }


# ======================================================
# DELETE ANNOUNCEMENT
# ======================================================

@router.delete("/{announcement_id}")
def api_delete_announcement(announcement_id: int):
    deleted = delete_announcement(announcement_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Announcement not found"
        )

    return {
        "success": True,
        "message": "Announcement deleted"
    }