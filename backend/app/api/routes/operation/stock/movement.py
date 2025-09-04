from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from app.api.dependencies import (
    SessionDep, CurrentUserDep, verify_area_access, 
)
from app.schemas.operation.stock_schema import (
    StockMovementCreate,
    StockMovementRead,
)
from app.crud.operation_crud import StockManager

router = APIRouter(prefix="/stock", tags=["movement"])


@router.post("/", response_model=StockMovementRead, status_code=status.HTTP_201_CREATED)
async def create(
    data: StockMovementCreate,
    session: SessionDep,
    user: CurrentUserDep
    ):  
    verify_area_access(data.area_id, user)
    manager = StockManager(session)
    try:
        stock = await manager.update_stock(data)
        return stock
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{movement_id}", response_model=StockMovementRead)
async def read(
    movement_id: int,
    session: SessionDep,
    user: CurrentUserDep
):
    manager = StockManager(session)
    movement = await manager.get_stock_movement(movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Stock movement not found")
    verify_area_access(movement.area_id, user)
    return movement


@router.delete("/{movement_id}", status_code=204)
async def cancel(
    movement_id: int,
    session: SessionDep,
    user: CurrentUserDep
):
    manager = StockManager(session)
    movement_db = await manager.get_stock_movement(movement_id)
    verify_area_access(movement_db.area_id, user)
    try:
        await manager.cancel_movement_stock(movement_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return


@router.get("/product/{product_id}/history", response_model=List[StockMovementRead])
async def product_track(
    product_id: int ,
    area_id:int ,
    date_begin: datetime ,
    date_end: datetime ,
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 10,
):
    verify_area_access(area_id, current_user)
    manager = StockManager(session)
    result = await manager.product_stock_track(product_id, area_id, date_begin, date_end, skip, limit)
    return result
