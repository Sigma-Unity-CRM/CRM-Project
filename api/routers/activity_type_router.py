from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.activity_type_queries import (
    ActivityTypeQueries,
    ActivityTypeDoesNotExist,
    ActivityTypeDatabaseError,
    ActivityTypeCreationError,
)
from models.activity_type import ActivityType, ActivityTypeCreate

router = APIRouter(tags=["Activity Type"], prefix="/api/activity-types")


@router.get("/")
async def get_all_activity_types(
    queries: ActivityTypeQueries = Depends(),
) -> list[ActivityType]:
    try:
        activity_types = queries.get_all_activity_types()
        return activity_types
    except ActivityTypeDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve activity types."
        )


@router.get("/{activity_type_id}")
def get_activity_type(
    activity_type_id: int, queries: ActivityTypeQueries = Depends()
) -> ActivityType:
    try:
        activity_type = queries.get_activity_type(activity_type_id)
        return activity_type
    except ActivityTypeDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity type not found")
    except ActivityTypeDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve activity type.",
        )


@router.post("/")
def create_activity_type(
    activity_type: ActivityTypeCreate, queries: ActivityTypeQueries = Depends()
) -> ActivityType:
    try:
        new_activity_type = queries.create_activity_type(activity_type)
        return new_activity_type
    except ActivityTypeCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ActivityTypeDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{activity_type_id}")
def delete_activity_type(
    activity_type_id: int,
    queries: ActivityTypeQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_activity_type(activity_type_id)
        if not success:
            raise ActivityTypeDoesNotExist(
                f"Activity type with id {activity_type_id} does not exist."
            )
        return {"status": "Activity type deleted successfully."}
    except ActivityTypeDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity type not found.")
    except ActivityTypeDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error deleting activity type.",
        )


@router.put("/{activity_type_id}")
def update_activity_type(
    activity_type_id: int,
    type_name: Optional[str] = None,
    description: Optional[str] = None,
    queries: ActivityTypeQueries = Depends(),
) -> ActivityType:
    try:
        updated_activity_type = queries.edit_activity_type(
            activity_type_id=activity_type_id,
            type_name=type_name,
            description=description,
        )
        return updated_activity_type
    except ActivityTypeDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity type not found.")
    except ActivityTypeDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error updating activity type.",
        )
