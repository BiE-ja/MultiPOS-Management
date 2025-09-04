
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.management.unit_schema import ( EmployeeCreate, EmployeeRead, EmployeeUpdate,)
from app.api.dependencies import SessionDep, CurrentUserDep, require_superuser_or_owner, verify_area_access
from app.crud.management_crud import POS_Manager
from app.models.utils import Message



router = APIRouter(prefix="/unit", tags=["employee"])


    
@router.get("/employee/{area_id}/{employee_id}", 
            dependencies=[Depends(require_superuser_or_owner)], 
            response_model= EmployeeRead )
async def read (area_id: int, employee_id:int, session: SessionDep, owner: CurrentUserDep):
    if not owner.is_superuser :
        verify_area_access(area_id, owner)  
    return await POS_Manager(session).get_Employee(employee_id)

@router.post("/employee/{area_id}", 
             dependencies=[Depends(require_superuser_or_owner)], 
             response_model= EmployeeRead, status_code=status.HTTP_201_CREATED )
async def create(area_id:int, employee_new: EmployeeCreate, session:SessionDep, owner: CurrentUserDep):
    if not owner.is_superuser:
        verify_area_access(area_id, owner)
    return await POS_Manager(session).create_Employee(employee_new)

@router.put("/employee/{area_id}/{employee_id}", 
            dependencies=[Depends(require_superuser_or_owner)], 
            response_model= EmployeeRead)
async def update(
    area_id:int, employee_id:int, 
    employee_update : EmployeeUpdate, 
    session: SessionDep, 
    user: CurrentUserDep 
    ):
    if not user.is_superuser:
        verify_area_access(area_id, user)
    try:
        return await POS_Manager(session).update_Employee(employee_id, employee_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/employee/{area_id}/{employee_id}", 
               dependencies=[Depends(require_superuser_or_owner)], response_model=Message)
async def delete(area_id:int,employee_id:int, session: SessionDep, user: CurrentUserDep ):
    if not user.is_superuser:
        verify_area_access(area_id, user)
    try:
        await POS_Manager(session).delete_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Message(message= "Employee with id: {area_id} have been delete successfuly")
# get employee by name



