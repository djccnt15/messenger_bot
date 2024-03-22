from contextlib import asynccontextmanager

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import configs

db_config = configs.config.db

SQLALCHEMY_DATABASE_URL = URL.create(**db_config.url)

engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    **db_config.engine,
)


@asynccontextmanager
async def get_db():
    db = AsyncSession(bind=engine)
    try:
        yield db
    finally:
        await db.close()
