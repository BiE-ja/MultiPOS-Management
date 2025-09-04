from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.core.config import settings


engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(expire_on_commit=False, bind=engine)
Base = declarative_base()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
