from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.api.deps import SessionDep
from backend.app.crud import people_crud
from app.core.config import settings
from app.models.utils import Token
from app.core import security

router = APIRouter()

@router.post("/token")
def login(db: SessionDep,form_data : Annotated[OAuth2PasswordRequestForm, Depends()]) ->Token:
    user = people_crud.authenticate(
        session=db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail ="Incorrect email or password")
    elif not user.is_active: # type: ignore
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token = security.create_access_token(
            user.id, expires_delta = access_token_expires
        )
    )