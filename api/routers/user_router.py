from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.user_queries import (
    UserQueries,
    UserDoesNotExist,
    UserDatabaseError,
    UserCreationError,
)
from models.user import User, UserCreate

router = APIRouter(tags=["User"], prefix="/api/users")


@router.get("/")
async def get_all_users(
    queries: UserQueries = Depends(),
) -> list[User]:
    try:
        users = queries.get_all_users()
        return users
    except UserDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve users.",
        )


@router.get("/{user_id}")
def get_user(user_id: int, queries: UserQueries = Depends()) -> User:
    try:
        user = queries.get_user(user_id)
        return user
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except UserDatabaseError:
        raise HTTPException(status_code=500, detail="Failed to retrieve user.")


@router.post("/")
def create_user(user: UserCreate, queries: UserQueries = Depends()) -> User:
    try:
        new_user = queries.create_user(user)
        return new_user
    except UserCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    queries: UserQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_user(user_id)
        if not success:
            raise UserDoesNotExist(f"User with id {user_id} does not exist.")
        return {"status": "User deleted successfully."}
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found.")
    except UserDatabaseError:
        raise HTTPException(status_code=500, detail="Error deleting user.")


@router.put("/{user_id}")
def update_user(
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    hashed_password: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    queries: UserQueries = Depends(),
) -> User:
    try:
        updated_user = queries.edit_user(
            user_id=user_id,
            username=username,
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )
        return updated_user
    except UserDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found.")
    except UserDatabaseError:
        raise HTTPException(status_code=500, detail="Error updating user.")
