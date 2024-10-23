from fastapi import APIRouter, Depends, HTTPException
from queries.activity_contact_queries import (
    ActivityContactQueries,
    ActivityContactDoesNotExist,
    ActivityContactDatabaseError,
)
from models.activity_contact import ActivityContact

router = APIRouter(tags=["Activity Contact"], prefix="/api/activity-contacts")


@router.get("/")
async def get_all_activity_contacts(
    queries: ActivityContactQueries = Depends(),
) -> list[ActivityContact]:
    try:
        activity_contacts = queries.get_all_activity_contacts()
        return activity_contacts
    except ActivityContactDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve activity contacts."
        )


@router.get("/{activity_id}/{contact_id}")
def get_activity_contact(
    activity_id: int, contact_id: int, queries: ActivityContactQueries = Depends()
) -> ActivityContact:
    try:
        activity_contact = queries.get_activity_contact(
            activity_id,
            contact_id,
        )
        return activity_contact
    except ActivityContactDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Activity contact not found",
        )
    except ActivityContactDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve activity contact."
        )


@router.post("/")
def create_activity_contact(
    activity_id: int, contact_id: int, queries: ActivityContactQueries = Depends()
) -> ActivityContact:
    try:
        new_activity_contact = queries.create_activity_contact(
            activity_id,
            contact_id,
        )
        return new_activity_contact
    except ActivityContactDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{activity_id}/{contact_id}")
def delete_activity_contact(
    activity_id: int,
    contact_id: int,
    queries: ActivityContactQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_activity_contact(activity_id, contact_id)
        if not success:
            raise ActivityContactDoesNotExist(
                f"Activity contact with activity {activity_id} and contact {contact_id} does not exist."
            )
        return {"status": "Activity contact deleted successfully."}
    except ActivityContactDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Activity contact not found.",
        )
    except ActivityContactDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error deleting activity contact.",
        )


@router.put("/{activity_id}/{contact_id}")
def update_activity_contact(
    activity_id: int, contact_id: int, queries: ActivityContactQueries = Depends()
) -> ActivityContact:
    try:
        updated_activity_contact = queries.edit_activity_contact(
            activity_id=activity_id,
            contact_id=contact_id,
        )
        return updated_activity_contact
    except ActivityContactDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Activity contact not found.",
        )
    except ActivityContactDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error updating activity contact.",
        )
