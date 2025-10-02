from sqlalchemy.ext.asyncio import AsyncSession


# Make sure all SQLAlchemy models are imported (app.models) before initializing DB
# otherwise, SQLAlchemy might fail to initialize relationships properly


async def init_db(session: AsyncSession):
    # local import to avoid circular dependencies
    from app.core.config import settings
    from app.dto.crud.management_crud import POS_Manager
    from app.dto.schemas.management.unit_schema import UserCreate

    # Tables should be created with Alembic migrations
    # add info of superuser in db
    user = await POS_Manager(session).get_user_by_email(email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            is_superuser=True,
            is_active=True,
            is_owner=False,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            last_name="Admin",
            phone="XXX-XX-XXX-XX",
        )
        user = await POS_Manager(session).createUser(user_in)

    return user
