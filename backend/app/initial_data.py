import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import engine
from app.core.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init():
    async with AsyncSession(engine) as session:
        await init_db(session)


async def main():
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")
