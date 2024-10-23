from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.account_queries import (
    AccountQueries,
    AccountDoesNotExist,
    AccountDatabaseError,
    AccountCreationError,
)
from models.account import Account, AccountCreate

router = APIRouter(tags=["Account"], prefix="/api/accounts")


@router.get("/")
async def get_all_accounts(
    queries: AccountQueries = Depends(),
) -> list[Account]:
    try:
        accounts = queries.get_all_accounts()
        return accounts
    except AccountDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve accounts.",
        )


@router.get("/{account_id}")
def get_account(account_id: int, queries: AccountQueries = Depends()) -> Account:
    try:
        account = queries.get_account(account_id)
        return account
    except AccountDoesNotExist:
        raise HTTPException(status_code=404, detail="Account not found")
    except AccountDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve account.",
        )


@router.post("/")
def create_account(
    account: AccountCreate, queries: AccountQueries = Depends()
) -> Account:
    try:
        new_account = queries.create_account(account)
        return new_account
    except AccountCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AccountDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    queries: AccountQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_account(account_id)
        if not success:
            raise AccountDoesNotExist(
                f"Account with id {account_id} does not exist.",
            )
        return {"status": "Account deleted successfully."}
    except AccountDoesNotExist:
        raise HTTPException(status_code=404, detail="Account not found.")
    except AccountDatabaseError:
        raise HTTPException(status_code=500, detail="Error deleting account.")


@router.put("/{account_id}")
def update_account(
    account_id: int,
    account_name: Optional[str] = None,
    website: Optional[str] = None,
    type: Optional[str] = None,
    description: Optional[str] = None,
    primary_phone: Optional[str] = None,
    secondary_phone: Optional[str] = None,
    billing_street_1: Optional[str] = None,
    billing_street_2: Optional[str] = None,
    billing_city: Optional[str] = None,
    billing_state: Optional[str] = None,
    billing_zipcode: Optional[str] = None,
    billing_country_id: Optional[int] = None,
    shipping_street_1: Optional[str] = None,
    shipping_street_2: Optional[str] = None,
    shipping_city: Optional[str] = None,
    shipping_state: Optional[str] = None,
    shipping_zipcode: Optional[str] = None,
    shipping_country_id: Optional[int] = None,
    account_owner_id: Optional[int] = None,
    queries: AccountQueries = Depends(),
) -> Account:
    try:
        updated_account = queries.edit_account(
            account_id=account_id,
            account_name=account_name,
            website=website,
            type=type,
            description=description,
            primary_phone=primary_phone,
            secondary_phone=secondary_phone,
            billing_street_1=billing_street_1,
            billing_street_2=billing_street_2,
            billing_city=billing_city,
            billing_state=billing_state,
            billing_zipcode=billing_zipcode,
            billing_country_id=billing_country_id,
            shipping_street_1=shipping_street_1,
            shipping_street_2=shipping_street_2,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_zipcode=shipping_zipcode,
            shipping_country_id=shipping_country_id,
            account_owner_id=account_owner_id,
        )
        return updated_account
    except AccountDoesNotExist:
        raise HTTPException(status_code=404, detail="Account not found.")
    except AccountDatabaseError:
        raise HTTPException(status_code=500, detail="Error updating account.")
