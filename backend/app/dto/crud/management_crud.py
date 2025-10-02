from typing import Literal
import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, insert, select, func
from sqlalchemy.orm import selectinload, aliased
from app.dto.models.models import Area, Employee, Role, User, area_owners
from app.dto.schemas.management.unit_schema import (
    AreaCreate,
    AreaUpdate,
    EmployeeCreate,
    EmployeeUpdate,
    RoleBase,
    RoleCreate,
    UpdatedPassword,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.api.utils import getSortableFields
from app.core.security import get_password_hash, verify_password


class POS_Manager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_area(self, area: AreaCreate):
        db_area = Area(name=area.name, location=area.location)

        self.db.add(db_area)
        try:
            await self.db.commit()
        except InterruptedError:
            await self.db.rollback()
            raise ValueError("Point of sale with this id already exist!")
        await self.db.refresh(db_area)
        # mise à jour de la jointure
        stmt = insert(area_owners).values(user_id=area.owner_id, area_id=db_area.id)
        await self.db.execute(stmt)
        return db_area

    async def get_Area(self, area_id: uuid.UUID):
        result = await self.db.get(Area, area_id)
        if not result:
            raise ValueError("Area not found")
        return result

    async def update_Area(self, area_id: uuid.UUID, area_update: AreaUpdate):
        db_area = await self.get_Area(area_id)
        for var, value in area_update.model_dump(exclude_unset=True).items():
            setattr(db_area, var, value)
        await self.db.commit()
        await self.db.refresh(db_area)
        return db_area

    async def delete_area(self, area_id: uuid.UUID):
        db_area = await self.get_Area(area_id)
        if db_area:
            await self.db.delete(db_area)
            await self.db.commit()
        return None

    # obtain list of area managed by a user
    async def list_managed_area(self, owner_id: uuid.UUID, skip: int = 0, limit: int = 10):
        # Alias pour éviter les ambiguïtés
        employee_user = aliased(User)

        stmt = (
            select(
                Area.id,
                Area.name,
                Area.location,
                func.count(Employee.id.distinct()).label("employee_count"),
                func.count(employee_user.id.distinct()).label("user_count"),
            )
            # 1. Join pour les area appartenant à ce owner
            .join(area_owners, area_owners.c.area_id == Area.id)
            .where(area_owners.c.user_id == owner_id)  # Paramètre de ta fonction
            # 2. Left join avec les employés de cette area
            .outerjoin(Employee, Employee.area_id == Area.id)
            # 3. Left join avec les users liés aux employés (ceux ayant un compte)
            .outerjoin(employee_user, employee_user.employee_id == Employee.id)
            # 4. Group by l'area pour les agrégats
            .group_by(Area.id, Area.name, Area.location)
            .offset(skip)
            .limit(limit)
        )
        # stmt = select(Area).where(Area.owners == owner_id).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # async def count_pos(self, owner_id: uuid.UUID):
    #    stmt = select(area_owners).where(area_owners. == owner_id)
    #    result = await self.db.execute(stmt)
    #    return len(result.scalars().all())

    async def create_Employee(self, new_employee: EmployeeCreate):
        db_employee = Employee(**new_employee.model_dump())
        self.db.add(db_employee)
        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee

    async def get_Employee(self, employee_id: uuid.UUID):
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        if not result:
            raise ValueError("Employee not found")
        return result.scalar_one_or_none()

    async def update_Employee(self, employee_id: uuid.UUID, employee_update: EmployeeUpdate):
        db_employee = await self.get_Employee(employee_id)
        if db_employee:
            for var, value in employee_update.model_dump(exclude_unset=True).items():
                setattr(db_employee, var, value)
            self.db.add(db_employee)
            await self.db.commit()
            await self.db.refresh(db_employee)
        return db_employee

    async def delete_employee(self, employee_id: uuid.UUID):
        db_employee = await self.get_Employee(employee_id)
        if db_employee:
            await self.db.delete(db_employee)
            await self.db.commit()
        return None

    async def get_area_employees_list(self, area_id: uuid.UUID, skip: int, limit: int):
        stmt = select(Employee).where(Employee.area_id == area_id).order_by(Employee.name).offset(skip).limit(limit)
        resultat = await self.db.execute(stmt)
        return resultat.scalars().all()

    async def create_Role(self, new_role: RoleCreate):
        db_role = Role(**new_role.model_dump())
        self.db.add(db_role)
        await self.db.commit()
        await self.db.refresh(db_role)
        return db_role

    async def get_Role(self, role_id: uuid.UUID):
        result = await self.db.execute(select(Role).where(Role.id == role_id))
        return result.scalar_one_or_none()

    async def update_Role(self, role_id: uuid.UUID, role_update: RoleBase):
        db_role = await self.get_Role(role_id)
        if db_role:
            for var, value in role_update.model_dump(exclude_unset=True).items():
                setattr(db_role, var, value)
            self.db.add(db_role)
            await self.db.commit()
            await self.db.refresh(db_role)
        return db_role

    async def delete_Role(self, role_id: uuid.UUID):
        db_role = await self.get_Role(role_id)
        if db_role:
            await self.db.delete(db_role)
            await self.db.commit()
        return None

    async def get_area_role_list(self, area_id: uuid.UUID, skip: int, limit: int):
        stmt = select(Role).where(Role.area_id == area_id).order_by(Role.name).offset(skip).limit(limit)
        resultat = await self.db.execute(stmt)
        return resultat.scalars().all()

    async def createUser(self, new_user: UserCreate) -> User:
        # Récupération du mot de passe
        password = new_user.password
        # transformation du modèle pydantic en modèle sqlAlchemy
        new_user = User(**new_user.model_dump())
        # vérification si un utilisateur avec l'email existe déjà
        db_user = await self.get_user_by_email(new_user.email)
        if isinstance(db_user, User) and new_user.id != db_user.id:
            raise HTTPException(status_code=409, detail="User with this email already exists")
        # transformation du mot de passe
        new_user.password = get_password_hash(password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def getUser(self, user_id: uuid.UUID):
        result = await self.db.execute(select(User).where(User.id == user_id))
        if not result:
            raise ValueError("User not found")
        return result.unique().scalar_one_or_none()

    async def updateUser(self, user_id: uuid.UUID, user_updated: UserUpdate):
        db_user = await self.getUser(user_id)
        if db_user:
            user_data = user_updated.model_dump(exclude_unset=True)
            for var, value in user_data.items():
                setattr(db_user, var, value)
            if "password" in user_data:
                db_user.password = get_password_hash(user_data["password"])
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
        return db_user

    async def update_password_me(self, user: User, pwd: UpdatedPassword):
        if not verify_password(pwd.current_password, user.password):
            raise ValueError("Incorrect password")
        if pwd.current_password == pwd.new_password:
            raise ValueError("New password cannot be the same as the current one")
        user.password = get_password_hash(pwd.new_password)
        self.db.add(user)
        await self.db.commit()
        return user

    async def update_user_me(self, user_updated: UserRead):
        user = await self.getUser(user_updated.id)
        if user is not None:
            user.name = user_updated.name
            user.last_name = user_updated.last_name
            user.email = user_updated.email
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def deleteUser(self, user_id: uuid.UUID):
        db_user = await self.getUser(user_id)
        if db_user:
            await self.db.delete(db_user)
            await self.db.commit()
        return None

    async def get_area_users_list(self, area_id: uuid.UUID, skip: int, limit: int):
        stmt = select(User).where(User.area_id == area_id).offset(skip).limit(limit)
        resultat = await self.db.execute(stmt)
        return resultat.scalars().all()

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        session_user = await self.db.execute(statement)
        # puisqu'il y a des jointures déclaré en lazy-joigned, il faut ajouter la fonction unique()
        # avant d'appeler scalar. La cause est que la même instance d'objet est invoqué deux fois
        # une fois via la classe user, et la deuxième fois via la classe Role en jointure
        return session_user.unique().scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> User | None:
        db_user = await self.get_user_by_email(email=email)
        # if db_user is None
        if not isinstance(db_user, User):
            return None
        # if password doesn't match
        if not verify_password(password, db_user.password):
            return None
        return db_user

    async def get_all_user(self, skip: int, limit: int):
        statement = select(User).offset(skip).limit(limit)
        resultat = await self.db.execute(statement)
        return resultat.scalars().all()

    # owner management
    async def getAllOwners(
        self,
        sort_by: Literal["id", "last_name", "created_at"] = "id",
        order: Literal["asc", "desc"] = "asc",
        skip: int = 0,
        limit: int = 10,
    ):

        sort_column = getSortableFields()[sort_by]

        if not sort_column:
            raise ValueError("Invalid sort field")

        order_func = asc if order == "asc" else desc

        statement = (
            select(User)
            .options(  # to avoid multiple queries for relationships
                selectinload(User.owned_areas),
                selectinload(User.employee),
                selectinload(User.roles),
            )
            .where(User.is_owner)
            .order_by(order_func(sort_column))
            .offset(skip)
            .limit(limit)
        )
        session_user = await self.db.execute(statement)
        return session_user.unique().scalars().all()


# class SaleManager
class SaleManager:
    def __init__(self, db: AsyncSession):
        self.db = db


# class PurchaseManager


# class InvoiceManager
