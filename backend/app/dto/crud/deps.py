import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password
from app.dto.schemas.management.unit_schema import UserCreate, UserUpdate
from app.dto.models.models import User


class UserManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def createUser(self, data: UserCreate):
        user = User(
            fullname=data.last_name,
            email=data.email,
            is_active=False,
            is_superuser=False,
            hashed_password=get_password_hash(data.password),
        )
        self.db.add(user)
        await self.db.commit()
        return user

    async def update_user(self, user_id: uuid.UUID, user_in: UserUpdate):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()
        # If the user is not found, raise an error
        # If the user is found, update the user with the new data
        # The user_in object is expected to be a UserUpdate schema instance.
        if not user:
            raise ValueError("User not found")

        for var, value in user_in.model_dump(exclude_unset=True):
            setattr(user, var, value)

        if user_in.password is not None:
            user.password = get_password_hash(user_in.password)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """Get a user by email"""
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def authenticate(self, email: str, password: str) -> User | None:
        db_user = await self.get_user_by_email(email=email)
        if not db_user:
            return None
        if not verify_password(password, db_user.password):
            return None
        return db_user
