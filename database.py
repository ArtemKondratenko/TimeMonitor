from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)
from model.base import DatabaseModel
from typing import AsyncGenerator




_engine = create_async_engine("sqlite+aiosqlite:///database.sql")
_async_session = async_sessionmaker(_engine)


async def init_database():
    async with _engine.begin() as conn:
        await conn.run_sync(DatabaseModel.metadata.create_all)

@asynccontextmanager
async def get_session_in_context() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session() as session:
        yield session
        await session.commit()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with _async_session() as session:
        yield session
        await session.commit()
