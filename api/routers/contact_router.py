from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.contact_queries import (
    ContactQueries,
    ContactDoesNotExist,
    ContactDatabaseError,
    ContactCreationError,
)
from models.contact import Contact, ContactCreate

router = APIRouter(tags=["Contact"], prefix="/api/contacts")


@router.get("/")
async def get_all_contacts(
    queries: ContactQueries = Depends(),
) -> list[Contact]:
    try:
        contacts = queries.get_all_contacts()
        return contacts
    except ContactDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve contacts.",
        )


@router.get("/{contact_id}")
def get_contact(contact_id: int, queries: ContactQueries = Depends()) -> Contact:
    try:
        contact = queries.get_contact(contact_id)
        return contact
    except ContactDoesNotExist:
        raise HTTPException(status_code=404, detail="Contact not found")
    except ContactDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve contact.",
        )


@router.post("/")
def create_contact(
    contact: ContactCreate, queries: ContactQueries = Depends()
) -> Contact:
    try:
        new_contact = queries.create_contact(contact)
        return new_contact
    except ContactCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ContactDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    queries: ContactQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_contact(contact_id)
        if not success:
            raise ContactDoesNotExist(
                f"Contact with id {contact_id} does not exist.",
            )
        return {"status": "Contact deleted successfully."}
    except ContactDoesNotExist:
        raise HTTPException(status_code=404, detail="Contact not found.")
    except ContactDatabaseError:
        raise HTTPException(status_code=500, detail="Error deleting contact.")


@router.put("/{contact_id}")
def update_contact(
    contact_id: int,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    title: Optional[str] = None,
    email: Optional[str] = None,
    primary_phone: Optional[str] = None,
    secondary_phone: Optional[str] = None,
    site_name: Optional[str] = None,
    site_street_1: Optional[str] = None,
    site_street_2: Optional[str] = None,
    site_city: Optional[str] = None,
    site_state: Optional[str] = None,
    site_zipcode: Optional[str] = None,
    site_country_id: Optional[int] = None,
    queries: ContactQueries = Depends(),
) -> Contact:
    try:
        updated_contact = queries.edit_contact(
            contact_id=contact_id,
            first_name=first_name,
            last_name=last_name,
            title=title,
            email=email,
            primary_phone=primary_phone,
            secondary_phone=secondary_phone,
            site_name=site_name,
            site_street_1=site_street_1,
            site_street_2=site_street_2,
            site_city=site_city,
            site_state=site_state,
            site_zipcode=site_zipcode,
            site_country_id=site_country_id,
        )
        return updated_contact
    except ContactDoesNotExist:
        raise HTTPException(status_code=404, detail="Contact not found.")
    except ContactDatabaseError:
        raise HTTPException(status_code=500, detail="Error updating contact.")
