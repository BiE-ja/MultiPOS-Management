from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class AreaBase(BaseModel):
    name: str
    location: Optional[str] = None
    owner_id: Optional[uuid.UUID] = None


class AreaCreate(AreaBase):
    pass


class AreaUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]


class AreaRead(AreaBase):

    id: uuid.UUID
    model_config = {"from_attributes": True}


class AreaDetails(AreaBase):
    id: uuid.UUID
    employee_count: int = 0
    user_count: int = 0
    created_at: datetime | None = None
    model_config = {"from_attributes": True}


# Schema for Employee and his Role


class RoleBase(BaseModel):
    name: str
    description: str | None
    permission: List[str] | None


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: uuid.UUID
    model_config = {"from_attributes": True}


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str | None
    phone: str
    adress: str


class EmployeeCreate(EmployeeBase):
    area_id: uuid.UUID


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    adress: str | None = None


class EmployeeRead(EmployeeBase):
    id: uuid.UUID
    area_id: uuid.UUID
    user_id: uuid.UUID | None
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
    employee_id: uuid.UUID | None = None


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserUpdate(BaseModel):
    name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_password_reinitialized: bool | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    is_owner: bool | None = None
    phone: str | None = None
    owned_ares: List[AreaUpdate] | None = None
    roles: List[RoleRead] | None = None


class UserRead(UserBase):
    id: uuid.UUID
    is_password_reinitialized: bool
    owned_areas: Optional[List[AreaRead]] = None
    employee: EmployeeRead | None
    roles: List[RoleRead]

    model_config = {"from_attributes": True}


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
    id: uuid.UUID
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
    id: uuid.UUID
    username: str

    model_config = {"from_attributes": True}
