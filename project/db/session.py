from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings

_engine = create_async_engine(settings.db_url)

async_session = async_sessionmaker(bind=_engine)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session

        await session.commit()
