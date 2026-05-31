from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

async_engine = create_async_engine(settings.database_url, echo=False)

sync_engine = create_engine(settings.database_url_sync, echo=False)

async_session_factory = async_sessionmaker(async_engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_factory() as session:
        yield session


def init_db():
    import app.models  # noqa: F401 — register tables in Base.metadata
    Base.metadata.create_all(bind=sync_engine)
