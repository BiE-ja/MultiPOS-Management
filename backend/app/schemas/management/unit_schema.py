from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class AreaBase(BaseModel):
    name: str
    location: Optional[str] = None
    owner_id: Optional[int] = None


class AreaCreate(AreaBase):
    pass


class AreaUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]


class AreaRead(AreaBase):
    id: int

    class config:
        orm_mode = True


# Schema for Employee and his Role


class RoleBase(BaseModel):
    name: str
    description: str | None
    permission: List[str] | None


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int
    model_config = {"from_attributes": True}


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str | None
    phone: str
    adress: str


class EmployeeCreate(EmployeeBase):
    area_id: int


class EmployeeUpdate(BaseModel):
    first_name: str | None
    last_name: str | None
    phone: str | None
    adress: str | None


class EmployeeRead(EmployeeBase):
    id: int
    area_id: int
    user_id: int | None
    model_config = {"from_attributes": True}


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_owner: bool
    name: str | None = None
    last_name: str
    phone: str | None
    created_at: datetime | None = None


class UserCreate(UserBase):
    password: str
    employee_id: int | None = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserUpdate(BaseModel):
    name: str | None
    last_name: str | None = None
    email: EmailStr | None
    password: str | None
    is_password_reinitialized: bool | None
    is_active: bool | None
    is_superuser: bool | None
    is_owner: bool | None
    phone: str | None
    owned_ares: List[AreaUpdate] | None
    roles: List[RoleRead] | None


class UserRead(UserBase):
    id: int
    is_password_reinitialized: bool
    owned_areas: List[AreaRead] | None = None
    employee: EmployeeRead | None
    roles: List[RoleRead]

    class config:
        orm_mode = True


class UsersRead(BaseModel):
    data: list[UserRead]
    count: int
    model_config = {"from_attributes": True}


class OwnersRead(BaseModel):
    data: list[UserRead]
    total: int
    total_active: int
    total_pos: int
    model_config = {"from_attributes": True}


class UserUpdateMe(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
    model_config = {"from_attributes": True}


class UpdatedPassword(BaseModel):
    current_password: str
    new_password: str


class UserAuth(UserPublic):
    roles: List[RoleRead]


class CustomerBase(BaseModel):
    nom: str
    email: str


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int
    username: str

    class Config:
        orm_mode = True
