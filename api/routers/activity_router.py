from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.activity_queries import (
    ActivityQueries,
    ActivityDoesNotExist,
    ActivityDatabaseError,
    ActivityCreationError,
)
from models.activity import Activity, ActivityCreate

router = APIRouter(tags=["Activity"], prefix="/api/activities")


@router.get("/")
async def get_all_activities(
    queries: ActivityQueries = Depends(),
) -> list[Activity]:
    try:
        activities = queries.get_all_activities()
        return activities
    except ActivityDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve activities.",
        )


@router.get("/{activity_id}")
def get_activity(activity_id: int, queries: ActivityQueries = Depends()) -> Activity:
    try:
        activity = queries.get_activity(activity_id)
        return activity
    except ActivityDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity not found")
    except ActivityDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve activity.",
        )


@router.post("/")
def create_activity(
    activity: ActivityCreate, queries: ActivityQueries = Depends()
) -> Activity:
    try:
        new_activity = queries.create_activity(activity)
        return new_activity
    except ActivityCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ActivityDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{activity_id}")
def delete_activity(
    activity_id: int,
    queries: ActivityQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_activity(activity_id)
        if not success:
            raise ActivityDoesNotExist(
                f"Activity with id {activity_id} does not exist."
            )
        return {"status": "Activity deleted successfully."}
    except ActivityDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity not found.")
    except ActivityDatabaseError:
        raise HTTPException(status_code=500, detail="Error deleting activity.")


@router.put("/{activity_id}")
def update_activity(
    activity_id: int,
    activity_type_id: Optional[int] = None,
    opportunity_id: Optional[int] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None,
    queries: ActivityQueries = Depends(),
) -> Activity:
    try:
        updated_activity = queries.edit_activity(
            activity_id=activity_id,
            activity_type_id=activity_type_id,
            opportunity_id=opportunity_id,
            description=description,
            due_date=due_date,
            completed=completed,
        )
        return updated_activity
    except ActivityDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity not found.")
    except ActivityDatabaseError:
        raise HTTPException(status_code=500, detail="Error updating activity.")
