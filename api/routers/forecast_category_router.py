from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.forecast_category_queries import (
    ForecastCategoryQueries,
    ForecastCategoryDoesNotExist,
    ForecastCategoryDatabaseError,
    ForecastCategoryCreationError,
)
from models.forecast_category import ForecastCategory, ForecastCategoryCreate

router = APIRouter(
    tags=["Forecast Category"],
    prefix="/api/forecast-categories",
)


@router.get("/")
async def get_all_forecast_categories(
    queries: ForecastCategoryQueries = Depends(),
) -> list[ForecastCategory]:
    try:
        forecast_categories = queries.get_all_forecast_categories()
        return forecast_categories
    except ForecastCategoryDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve forecast categories."
        )


@router.get("/{forecast_category_id}")
def get_forecast_category(
    forecast_category_id: int, queries: ForecastCategoryQueries = Depends()
) -> ForecastCategory:
    try:
        forecast_category = queries.get_forecast_category(forecast_category_id)
        return forecast_category
    except ForecastCategoryDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Forecast category not found",
        )
    except ForecastCategoryDatabaseError:
        raise HTTPException(
            status_code=500, detail="Failed to retrieve forecast category."
        )


@router.post("/")
def create_forecast_category(
    forecast_category: ForecastCategoryCreate,
    queries: ForecastCategoryQueries = Depends(),
) -> ForecastCategory:
    try:
        new_forecast_category = queries.create_forecast_category(
            forecast_category,
        )
        return new_forecast_category
    except ForecastCategoryCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ForecastCategoryDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{forecast_category_id}")
def delete_forecast_category(
    forecast_category_id: int,
    queries: ForecastCategoryQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_forecast_category(forecast_category_id)
        if not success:
            raise ForecastCategoryDoesNotExist(
                f"Forecast category {forecast_category_id} does not exist."
            )
        return {"status": "Forecast category deleted successfully."}
    except ForecastCategoryDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Forecast category not found.",
        )
    except ForecastCategoryDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error deleting forecast category.",
        )


@router.put("/{forecast_category_id}")
def update_forecast_category(
    forecast_category_id: int,
    category_name: Optional[str] = None,
    description: Optional[str] = None,
    queries: ForecastCategoryQueries = Depends(),
) -> ForecastCategory:
    try:
        updated_forecast_category = queries.edit_forecast_category(
            forecast_category_id=forecast_category_id,
            category_name=category_name,
            description=description,
        )
        return updated_forecast_category
    except ForecastCategoryDoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Forecast category not found.",
        )
    except ForecastCategoryDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Error updating forecast category.",
        )
