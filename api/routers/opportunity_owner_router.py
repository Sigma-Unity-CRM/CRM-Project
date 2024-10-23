from fastapi import APIRouter, Depends, HTTPException
from queries.opportunity_owner_queries import (
    OpportunityOwnerQueries,
    OpportunityOwnerDoesNotExist,
    OpportunityOwnerDatabaseError,
)
from models.opportunity_owner import OpportunityOwner

router = APIRouter(
    tags=["Opportunity Owner"],
    prefix="/api/opportunity-owners",
)


@router.get("/")
async def get_all_opportunity_owners(
    queries: OpportunityOwnerQueries = Depends(),
) -> list[OpportunityOwner]:
    try:
        opportunity_owners = queries.get_all_opportunity_owners()
        return opportunity_owners
    except OpportunityOwnerDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve opportunity owners."
        )


@router.get("/{opportunity_id}/{user_id}")
def get_opportunity_owner(
    opportunity_id: int, user_id: int, queries: OpportunityOwnerQueries = Depends()
) -> OpportunityOwner:
    try:
        opportunity_owner = queries.get_opportunity_owner(
            opportunity_id,
            user_id,
        )
        return opportunity_owner
    except OpportunityOwnerDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Opportunity owner not found",
        )
    except OpportunityOwnerDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve opportunity owner."
        )


@router.post("/")
def create_opportunity_owner(
    opportunity_id: int, user_id: int, queries: OpportunityOwnerQueries = Depends()
) -> OpportunityOwner:
    try:
        new_opportunity_owner = queries.create_opportunity_owner(
            opportunity_id, user_id
        )
        return new_opportunity_owner
    except OpportunityOwnerDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{opportunity_id}/{user_id}")
def delete_opportunity_owner(
    opportunity_id: int,
    user_id: int,
    queries: OpportunityOwnerQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_opportunity_owner(opportunity_id, user_id)
        if not success:
            raise OpportunityOwnerDoesNotExist(
                f"Opportunity owner with opportunity id {opportunity_id} and user id {user_id} does not exist."
            )
        return {"status": "Opportunity owner deleted successfully."}
    except OpportunityOwnerDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Opportunity owner not found.",
        )
    except OpportunityOwnerDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error deleting opportunity owner.",
        )


@router.put("/{opportunity_id}/{user_id}")
def update_opportunity_owner(
    opportunity_id: int, user_id: int, queries: OpportunityOwnerQueries = Depends()
) -> OpportunityOwner:
    try:
        updated_opportunity_owner = queries.edit_opportunity_owner(
            opportunity_id=opportunity_id,
            user_id=user_id,
        )
        return updated_opportunity_owner
    except OpportunityOwnerDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Opportunity owner not found.",
        )
    except OpportunityOwnerDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error updating opportunity owner.",
        )
