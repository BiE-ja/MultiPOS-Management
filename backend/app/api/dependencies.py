from typing import Annotated, List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from app.core.config import settings
from app.schemas.utils import TokenPayload
from app.schemas.management.unit_schema import UserRead
from app.core import security
from app.core.database import get_session
from jwt.exceptions import InvalidTokenError # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl = f"{settings.API_V01_STR}/login/access-token"
)

SessionDep = Annotated[AsyncSession, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session : SessionDep, token: TokenDep) -> UserRead:
    try:
        payload = security.decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = await session.get(UserRead, token_data.sub)
    # If the user is not found, raise an error
    # If the user is found, check if the user is active
    if not user:
        raise HTTPException(status_code=404, detail="user not found" )
    if not user.is_active :
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUserDep = Annotated[UserRead, Depends(get_current_user)]
    
async def get_current_active_superuser(current_user: CurrentUserDep)  ->UserRead:
   if not current_user.is_superuser:
       raise HTTPException(
           status_code=403, detail="The user doesn't have enough privileges"
       )   
   return current_user

CurrentSuperUser = Annotated[UserRead, get_current_active_superuser]

def get_user_area_scope(current_user: CurrentUserDep) -> Optional[List[int]]:
    if current_user.is_superuser:
        return None
    if current_user.is_owner and current_user.owned_areas:
        return [area.id for area in current_user.owned_areas]
    if current_user.employee and current_user.employee.area_id:
        return [current_user.employee.area_id]
    raise HTTPException(
        status_code= status.HTTP_403_FORBIDDEN, detail="The user doesn't have access defined"
    )

AreaScope = Annotated[Optional[List[int]], Depends(get_user_area_scope)]

def check_area_access (area_id : int, area_scope : AreaScope | None, current_user: UserRead):
    if not current_user.is_superuser:
        if area_scope is None or area_id not in area_scope:
            raise HTTPException(status_code=403, detail="Access denied!")

def verify_area_access (area_id:int, user: UserRead):
    async def _verify(area_scope: AreaScope):
        check_area_access(area_id, area_scope, user)
    return Depends(_verify)

def require_superuser_or_owner(user : CurrentUserDep):
    if not (user.is_superuser or user.is_owner):
        raise HTTPException(status_code=403, detail="Access denied!")