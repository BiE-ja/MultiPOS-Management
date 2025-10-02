import logging
import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init():
    from app.core.database import engine
    from app.core.init_db import init_db

    async with AsyncSession(engine) as session:
        await init_db(session)
        # logger.info("Info superuser: %s", user.email)


async def main():
    try:
        logger.info("Creating initial data")
        await init()
        logger.info("Initial data created")

    except Exception as e:
        logger.error("init failed: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
