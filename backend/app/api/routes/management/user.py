from typing import Any, Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status


from app.schemas.management.unit_schema import (
    OwnersRead,
    UpdatedPassword,
    UserAuth,
    UserCreate,
    UserPublic,
    UserRead,
    UserRegister,
    UserUpdate,
    UserUpdateMe,
    UsersPublic,
)
from app.api.dependencies import SessionDep, CurrentUserDep, require_superuser_or_owner, verify_area_access
from app.crud.management_crud import POS_Manager
from app.models.utils import Message
from app.models.management.unit import User


router = APIRouter(prefix="/unit", tags=["users"])


@router.get("/users/list/{area_id}", dependencies=[Depends(require_superuser_or_owner)], response_model=UsersPublic)
async def fetchAll(area_id: int, session: SessionDep, current_user: CurrentUserDep, skip: int = 0, limit: int = 10):
    """Get all users from area id
    List of all user for the area
    """
    verify_area_access(area_id, current_user)
    data = await POS_Manager(session).get_area_users_list(area_id, skip, limit)
    data_list = list(map(UserPublic.model_validate, data))
    return UsersPublic(data=data_list, count=len(data_list))


@router.get("/users/list/admin", response_model=UsersPublic)
async def fetchAllByAdmin(session: SessionDep, current_user: CurrentUserDep, skip: int = 0, limit: int = 10):
    """Get all users
    "List of all user for the area
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Access Denied.")
    data = await POS_Manager(session).get_all_user(skip, limit)
    data_list = list(map(UserPublic.model_validate, data))
    return UsersPublic(data=data_list, count=len(data_list))


@router.get("/user/{area_id}/{user_id}", dependencies=[Depends(require_superuser_or_owner)], response_model=UserPublic)
async def read(area_id: int, user_id: int, session: SessionDep, owner: CurrentUserDep):
    if not owner.is_superuser:
        verify_area_access(area_id, owner)
    try:
        return await POS_Manager(session).getUser(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/auth}", dependencies=[Depends(require_superuser_or_owner)], response_model=UserAuth)
async def auth(session: SessionDep, owner: CurrentUserDep, current_user: CurrentUserDep):
    return current_user


@router.get("/user/me}", dependencies=[Depends(require_superuser_or_owner)], response_model=UserPublic)
async def readMe(session: SessionDep, owner: CurrentUserDep, current_user: CurrentUserDep):
    return current_user


@router.post(
    "/user/{area_id}",
    dependencies=[Depends(require_superuser_or_owner)],
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create(area_id: int, user_new: UserCreate, session: SessionDep, owner: CurrentUserDep):
    if not owner.is_superuser:
        verify_area_access(area_id, owner)
    return await POS_Manager(session).createUser(user_new)


@router.put("/user/{area_id}/{user_id}", dependencies=[Depends(require_superuser_or_owner)], response_model=UserPublic)
async def update(area_id: int, user_id: int, user_update: UserUpdate, session: SessionDep, user: CurrentUserDep):
    if not user.is_superuser:
        verify_area_access(area_id, user)
    try:
        return await POS_Manager(session).updateUser(user_id, user_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("user/me", response_model=Message)
async def update_me(user: UserUpdateMe, session: SessionDep, current_user: CurrentUserDep):
    """Update do himself"""
    updated = False
    if user.last_name is not None:
        if user.last_name.lower() != (current_user.last_name or "").lower():
            current_user.last_name = user.last_name
            updated = True
    if user.name is not None:
        if current_user.name is not None and user.name.lower() != (current_user.name or "").lower():
            current_user.name = user.name
            updated = True
        elif current_user.name is None:
            current_user.name = user.name
            updated = True
    manager = POS_Manager(session)
    if user.email is not None:
        if user.email != (current_user.email or ""):
            existing_user = await manager.get_user_by_email(user.email)
            if existing_user is None:
                raise HTTPException(status_code=400, detail="User with this email already exist")
            current_user.email = user.email
            updated = True
    if not updated:
        return Message(message="Any modification detected")
    return await manager.update_user_me(current_user)


@router.patch("/user/me/password", response_model=Message)
async def update_password_me(pwd: UpdatedPassword, user_id: int, session: SessionDep, user: CurrentUserDep):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="Access Denied. Not enough privilege to do this action")
    manager = POS_Manager(session)
    updated_user = await manager.getUser(user.id)
    await manager.update_password_me(updated_user, pwd)
    return Message(message="Password updated")


@router.delete("/user/{area_id}/{user_id}", dependencies=[Depends(require_superuser_or_owner)], response_model=Message)
async def delete(area_id: int, user_id: int, session: SessionDep, user: CurrentUserDep):
    """Delete user
    the operation is do by the user owner of an area or by the superuser
    user owner can delete only user in his area scope
    """
    if not user.is_superuser:
        verify_area_access(area_id, user)
    elif user_id == user.id:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    try:
        await POS_Manager(session).deleteUser(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Message(message="User with id: {area_id} have been delete successfuly")


@router.delete("/user/me", response_model=Message)
async def delete_me(session: SessionDep, current_user: CurrentUserDep):
    """delete by himself"""
    if current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    await POS_Manager(session).deleteUser(current_user.id)
    return Message(message="Your deleted successfully")


@router.get("/user/{area_id}/{email}", dependencies=[Depends(require_superuser_or_owner)], response_model=UserPublic)
async def read_by_email(area_id: int, email: str, session: SessionDep, owner: CurrentUserDep):
    if not owner.is_superuser:
        verify_area_access(area_id, owner)
    user = await POS_Manager(session).get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/signup", response_model=UserPublic)
async def register(session: SessionDep, user_in: UserRegister) -> Any:
    """
    Create new user without the need to be logged in.
    """
    manager = POS_Manager(session)
    user = await manager.get_user_by_email(email=user_in.email)
    if isinstance(user, User):
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = await manager.createUser(user_create)
    return user


@router.get("/owners-list", response_model=OwnersRead)
async def ownersList(
    session: SessionDep,
    current_user: CurrentUserDep,
    sort_by: Literal["id", "last_name", "created_at"] = Query("id"),
    order: Literal["asc", "desc"] = Query("asc"),
    skip: int = 0,
    limit: int = 10,
):
    """Get all owners
    List of all owner
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Access Denied.")
    try:
        data = await POS_Manager(session).getAllOwners(sort_by, order, skip, limit)
        data_list = list(map(UserRead.model_validate, data))
        total_active = sum(owner.is_active for owner in data_list)
        total_pos = 0
        for owner in data_list:
            owner_count_pos = await POS_Manager(session).count_pos(owner.id)
            total_pos += owner_count_pos
        return OwnersRead(data=data_list, total=len(data_list), total_active=total_active, total_pos=total_pos)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
