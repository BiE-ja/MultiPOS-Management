from typing import List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from app.dto.schemas.management.unit_schema import AreaCreate, AreaDetails, AreaRead, AreaUpdate, UsersPublic
from app.api.dependencies import (
    SessionDep,
    CurrentUserDep,
    require_superuser,
    require_superuser_or_owner,
    verify_area_access,
)
from app.dto.crud.management_crud import POS_Manager
from app.dto.models.utils import Message

router = APIRouter(prefix="/unit", tags=["Zone"])


@router.post("/", response_model=AreaRead, status_code=status.HTTP_201_CREATED)
async def create(data: AreaCreate, user: CurrentUserDep, session: SessionDep):
    if not user.is_owner:
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="You don't have enough privilege to do this action")
    manager = POS_Manager(session)
    try:
        area = await manager.create_area(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return area


@router.get("/{area_id}", response_model=AreaRead)
async def read(area_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep):
    verify_area_access(area_id, current_user)
    area = await POS_Manager(session).get_Area(area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Point of sale not found")
    return area


@router.delete("/{area_id}", response_model=Message)
async def delete(area_id: uuid.UUID, session: SessionDep, user: CurrentUserDep):
    verify_area_access(area_id, user)
    try:
        await POS_Manager(session).delete_area(area_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Message(message="Point of Sale with id: {area_id} have been delete successfuly")


@router.put("/{area_id}", dependencies=[Depends(require_superuser_or_owner)], response_model=UsersPublic)
async def update(area_id: uuid.UUID, area: AreaUpdate, session: SessionDep, owner: CurrentUserDep):
    verify_area_access(area_id, owner)
    manager = POS_Manager(session)
    try:
        return await manager.update_Area(area_id, area)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/list", dependencies=[Depends(require_superuser_or_owner)], response_model=List[AreaDetails])
async def list_all(session: SessionDep, user: CurrentUserDep):
    if user.is_superuser:
        raise HTTPException(
            status_code=403, detail="Please, select one owner for see his list of point of sale managed"
        )
    data = await POS_Manager(session).list_managed_area(user.id)
    return list(map(AreaRead.model_validate, data))


@router.get("/admin/list-pos-of/{user_id}", dependencies=[Depends(require_superuser)], response_model=List[AreaDetails])
async def list_all_by_admin(session: SessionDep, user_id: uuid.UUID):
    data = await POS_Manager(session).list_managed_area(user_id)
    return list(map(AreaDetails.model_validate, data))
