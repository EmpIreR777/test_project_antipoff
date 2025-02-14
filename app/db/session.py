import logging
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncSession
    )

from app.core.config import settings


engine = create_async_engine(url=settings.get_database_url())
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def get_db_session():
    """Асинхронный контекстный менеджер для работы с сессией БД."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logging.error(f"Database error: {str(e)}")
            raise