from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.country_queries import (
    CountryQueries,
    CountryDoesNotExist,
    CountryDatabaseError,
    CountryCreationError,
)
from models.country import Country, CountryCreate

router = APIRouter(tags=["Country"], prefix="/api/countries")


@router.get("/")
async def get_all_countries(
    queries: CountryQueries = Depends(),
) -> list[Country]:
    try:
        countries = queries.get_all_countries()
        return countries
    except CountryDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve countries.",
        )


@router.get("/{country_id}")
def get_country(country_id: int, queries: CountryQueries = Depends()) -> Country:
    try:
        country = queries.get_country(country_id)
        return country
    except CountryDoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found")
    except CountryDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve country.",
        )


@router.post("/")
def create_country(
    country: CountryCreate, queries: CountryQueries = Depends()
) -> Country:
    try:
        new_country = queries.create_country(country)
        return new_country
    except CountryCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except CountryDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{country_id}")
def delete_country(
    country_id: int,
    queries: CountryQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_country(country_id)
        if not success:
            raise CountryDoesNotExist(
                f"Country with id {country_id} does not exist.",
            )
        return {"status": "Country deleted successfully."}
    except CountryDoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found.")
    except CountryDatabaseError:
        raise HTTPException(status_code=500, detail="Error deleting country.")


@router.put("/{country_id}")
def update_country(
    country_id: int,
    country_name: Optional[str] = None,
    country_code: Optional[str] = None,
    queries: CountryQueries = Depends(),
) -> Country:
    try:
        updated_country = queries.edit_country(
            country_id=country_id,
            country_name=country_name,
            country_code=country_code,
        )
        return updated_country
    except CountryDoesNotExist:
        raise HTTPException(status_code=404, detail="Country not found.")
    except CountryDatabaseError:
        raise HTTPException(status_code=500, detail="Error updating country.")
