from fastapi import APIRouter, Depends, HTTPException
from queries.opportunity_contact_queries import (
    OpportunityContactQueries,
    OpportunityContactDoesNotExist,
    OpportunityContactDatabaseError,
)
from models.opportunity_contact import OpportunityContact

router = APIRouter(
    tags=["Opportunity Contact"],
    prefix="/api/opportunity-contacts",
)


@router.get("/")
async def get_all_opportunity_contacts(
    queries: OpportunityContactQueries = Depends(),
) -> list[OpportunityContact]:
    try:
        opportunity_contacts = queries.get_all_opportunity_contacts()
        return opportunity_contacts
    except OpportunityContactDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve opportunity contacts."
        )


@router.get("/{opportunity_id}/{contact_id}")
def get_opportunity_contact(
    opportunity_id: int, contact_id: int, queries: OpportunityContactQueries = Depends()
) -> OpportunityContact:
    try:
        opportunity_contact = queries.get_opportunity_contact(
            opportunity_id, contact_id
        )
        return opportunity_contact
    except OpportunityContactDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Opportunity contact not found",
        )
    except OpportunityContactDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve opportunity contact."
        )


@router.post("/")
def create_opportunity_contact(
    opportunity_id: int, contact_id: int, queries: OpportunityContactQueries = Depends()
) -> OpportunityContact:
    try:
        new_opportunity_contact = queries.create_opportunity_contact(
            opportunity_id, contact_id
        )
        return new_opportunity_contact
    except OpportunityContactDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{opportunity_id}/{contact_id}")
def delete_opportunity_contact(
    opportunity_id: int,
    contact_id: int,
    queries: OpportunityContactQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_opportunity_contact(
            opportunity_id,
            contact_id,
        )
        if not success:
            raise OpportunityContactDoesNotExist(
                f"Opportunity contact with opportunity id {opportunity_id} and contact id {contact_id} does not exist."
            )
        return {"status": "Opportunity contact deleted successfully."}
    except OpportunityContactDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Opportunity contact not found.",
        )
    except OpportunityContactDatabaseError:
        raise HTTPException(
            status_code=500, detail="Error deleting opportunity contact."
        )


@router.put("/{opportunity_id}/{contact_id}")
def update_opportunity_contact(
    opportunity_id: int, contact_id: int, queries: OpportunityContactQueries = Depends()
) -> OpportunityContact:
    try:
        updated_opportunity_contact = queries.edit_opportunity_contact(
            opportunity_id=opportunity_id,
            contact_id=contact_id,
        )
        return updated_opportunity_contact
    except OpportunityContactDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Opportunity contact not found.",
        )
    except OpportunityContactDatabaseError:
        raise HTTPException(
            status_code=500, detail="Error updating opportunity contact."
        )
