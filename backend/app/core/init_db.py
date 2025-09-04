from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# Make sure all SQLAlchemy models are imported (app.models) before initializing DB
# otherwise, SQLAlchemy might fail to initialize relationships properly


async def init_db(session: AsyncSession):
    # local import to avoid circular dependencies
    from core.config import settings
    from app.crud.deps import UserManager
    from backend.app.models.management.unit import User
    from backend.app.schemas.management.unit_schema import UserCreate

    # Tables should be created with Alembic migrations
    # add info of superuser in db
    resultat = await session.execute(select(User).where(User.email == settings.FIRST_SUPERUSER))
    user = resultat.scalar_one_or_none()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            is_superuser=True,
            is_active=False,
            is_owner=False,
            password=settings.FIRST_SUPERUSER,
            last_name="Admin",
            phone="XXX-XX-XXX-XX",
        )
        user = await UserManager(session).createUser(user_in)
    return user
