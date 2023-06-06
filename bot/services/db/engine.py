from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.services.db.db_base import Base
from bot.settings import Settings


async def create_db_session(cfg: Settings):
    engine = create_async_engine(
        url=cfg.DB_DSN,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=True, class_=AsyncSession,
    )

    return async_session
