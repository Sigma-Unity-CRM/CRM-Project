from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.opportunity_queries import (
    OpportunityQueries,
    OpportunityDoesNotExist,
    OpportunityDatabaseError,
    OpportunityCreationError,
)
from models.opportunity import Opportunity, OpportunityCreate

router = APIRouter(tags=["Opportunity"], prefix="/api/opportunities")


@router.get("/")
async def get_all_opportunities(
    queries: OpportunityQueries = Depends(),
) -> list[Opportunity]:
    try:
        opportunities = queries.get_all_opportunities()
        return opportunities
    except OpportunityDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve opportunities.",
        )


@router.get("/{opportunity_id}")
def get_opportunity(
    opportunity_id: int, queries: OpportunityQueries = Depends()
) -> Opportunity:
    try:
        opportunity = queries.get_opportunity(opportunity_id)
        return opportunity
    except OpportunityDoesNotExist:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    except OpportunityDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve opportunity.",
        )


@router.post("/")
def create_opportunity(
    opportunity: OpportunityCreate, queries: OpportunityQueries = Depends()
) -> Opportunity:
    try:
        new_opportunity = queries.create_opportunity(opportunity)
        return new_opportunity
    except OpportunityCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except OpportunityDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{opportunity_id}")
def delete_opportunity(
    opportunity_id: int,
    queries: OpportunityQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_opportunity(opportunity_id)
        if not success:
            raise OpportunityDoesNotExist(
                f"Opportunity with id {opportunity_id} does not exist."
            )
        return {"status": "Opportunity deleted successfully."}
    except OpportunityDoesNotExist:
        raise HTTPException(status_code=404, detail="Opportunity not found.")
    except OpportunityDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error deleting opportunity.",
        )


@router.put("/{opportunity_id}")
def update_opportunity(
    opportunity_id: int,
    opportunity_name: Optional[str] = None,
    stage_id: Optional[int] = None,
    forecast_category_id: Optional[int] = None,
    amount: Optional[float] = None,
    close_date: Optional[str] = None,
    description: Optional[str] = None,
    queries: OpportunityQueries = Depends(),
) -> Opportunity:
    try:
        updated_opportunity = queries.edit_opportunity(
            opportunity_id=opportunity_id,
            opportunity_name=opportunity_name,
            stage_id=stage_id,
            forecast_category_id=forecast_category_id,
            amount=amount,
            close_date=close_date,
            description=description,
        )
        return updated_opportunity
    except OpportunityDoesNotExist:
        raise HTTPException(status_code=404, detail="Opportunity not found.")
    except OpportunityDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error updating opportunity.",
        )
