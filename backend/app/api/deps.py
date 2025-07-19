from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from app.core.config import settings
from sqlalchemy.orm import Session
from backend.app.schemas.deps.utils_schema import TokenPayload
from backend.app.schemas.deps.people_schema import UserRead
from backend.app.core import security
from backend.app.database import get_db
from jwt.exceptions import InvalidTokenError # type: ignore

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl = f"{settings.API_V1_STR}/login/access-token"
)

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session : SessionDep, token: TokenDep) -> UserRead:
    try:
        payload = security.decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )
    user = session.get(UserRead, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="user not found" )
    if not user.is_active :
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[UserRead, Depends(get_current_user)]
    
def get_current_active_superuser(current_user: CurrentUser)  ->UserRead:
   if not current_user.is_superuser:
       raise HTTPException(
           status_code=403, detail="The user doesn't have enough privileges"
       )   
   return current_user



