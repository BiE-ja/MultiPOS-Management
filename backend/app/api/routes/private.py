from fastapi import APIRouter
from pydantic import BaseModel

from app.api.dependencies import SessionDep
from app.core.security import get_password_hash
from app.models.management.unit import User
from app.schemas.management.unit_schema import UserPublic


router = APIRouter(tags= ["private"], prefix = "/private")

class PrivateUserCreate(BaseModel):
    email: str
    password : str
    full_name : str
    is_verified:bool = False

@router.post("/users/", response_model=UserPublic)
async def create_user(user_in : PrivateUserCreate, session : SessionDep):
    user = User(
        email = user_in.email,
        full_name = user_in.full_name,
        hashed_password = get_password_hash(user_in.password),
    )
    session.add(user)
    await session.commit()
    return user