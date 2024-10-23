from fastapi import APIRouter, Depends, HTTPException
from queries.activity_user_queries import (
    ActivityUserQueries,
    ActivityUserDoesNotExist,
    ActivityUserDatabaseError,
)
from models.activity_user import ActivityUser

router = APIRouter(tags=["Activity User"], prefix="/api/activity-users")


@router.get("/")
async def get_all_activity_users(
    queries: ActivityUserQueries = Depends(),
) -> list[ActivityUser]:
    try:
        activity_users = queries.get_all_activity_users()
        return activity_users
    except ActivityUserDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve activity users."
        )


@router.get("/{activity_id}/{user_id}")
def get_activity_user(
    activity_id: int, user_id: int, queries: ActivityUserQueries = Depends()
) -> ActivityUser:
    try:
        activity_user = queries.get_activity_user(activity_id, user_id)
        return activity_user
    except ActivityUserDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity user not found")
    except ActivityUserDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve activity user.",
        )


@router.post("/")
def create_activity_user(
    activity_id: int, user_id: int, queries: ActivityUserQueries = Depends()
) -> ActivityUser:
    try:
        new_activity_user = queries.create_activity_user(activity_id, user_id)
        return new_activity_user
    except ActivityUserDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{activity_id}/{user_id}")
def delete_activity_user(
    activity_id: int,
    user_id: int,
    queries: ActivityUserQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_activity_user(activity_id, user_id)
        if not success:
            raise ActivityUserDoesNotExist(
                f"Activity user with activity {activity_id} and user {user_id} does not exist."
            )
        return {"status": "Activity user deleted successfully."}
    except ActivityUserDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity user not found.")
    except ActivityUserDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error deleting activity user.",
        )


@router.put("/{activity_id}/{user_id}")
def update_activity_user(
    activity_id: int, user_id: int, queries: ActivityUserQueries = Depends()
) -> ActivityUser:
    try:
        updated_activity_user = queries.edit_activity_user(
            activity_id=activity_id,
            user_id=user_id,
        )
        return updated_activity_user
    except ActivityUserDoesNotExist:
        raise HTTPException(status_code=404, detail="Activity user not found.")
    except ActivityUserDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error updating activity user.",
        )
