from typing import Optional
from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    nom: str
    email : str

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    username : str
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    is_active : bool
    is_superuser: bool
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserRegister (BaseModel):
    email : EmailStr
    password : str
    full_name: str | None = None

class UserUpdate(UserBase):
    email: Optional[EmailStr] # type: ignore
    password: Optional[str]

class UserRead(UserBase):
    id : int
    class config:
        orm_mode= True

class UserUpadateMe(BaseModel):
    full_name: str | None = None
    email: EmailStr| None = None
