from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from queries.stage_queries import (
    StageQueries,
    StageDoesNotExist,
    StageDatabaseError,
    StageCreationError,
)
from models.stage import Stage, StageCreate

router = APIRouter(tags=["Stage"], prefix="/api/stages")


@router.get("/")
async def get_all_stages(
    queries: StageQueries = Depends(),
) -> list[Stage]:
    try:
        stages = queries.get_all_stages()
        return stages
    except StageDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve stages.",
        )


@router.get("/{stage_id}")
def get_stage(stage_id: int, queries: StageQueries = Depends()) -> Stage:
    try:
        stage = queries.get_stage(stage_id)
        return stage
    except StageDoesNotExist:
        raise HTTPException(status_code=404, detail="Stage not found")
    except StageDatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve stage.",
        )


@router.post("/")
def create_stage(stage: StageCreate, queries: StageQueries = Depends()) -> Stage:
    try:
        new_stage = queries.create_stage(stage)
        return new_stage
    except StageCreationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except StageDatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{stage_id}")
def delete_stage(
    stage_id: int,
    queries: StageQueries = Depends(),
) -> dict:
    try:
        success = queries.delete_stage(stage_id)
        if not success:
            raise StageDoesNotExist(
                f"Stage with id {stage_id} does not exist.",
            )
        return {"status": "Stage deleted successfully."}
    except StageDoesNotExist:
        raise HTTPException(status_code=404, detail="Stage not found.")
    except StageDatabaseError:
        raise HTTPException(status_code=500, detail="Error deleting stage.")


@router.put("/{stage_id}")
def update_stage(
    stage_id: int,
    stage_name: Optional[str] = None,
    description: Optional[str] = None,
    queries: StageQueries = Depends(),
) -> Stage:
    try:
        updated_stage = queries.edit_stage(
            stage_id=stage_id,
            stage_name=stage_name,
            description=description,
        )
        return updated_stage
    except StageDoesNotExist:
        raise HTTPException(status_code=404, detail="Stage not found.")
    except StageDatabaseError:
        raise HTTPException(status_code=500, detail="Error updating stage.")
