from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class DatabaseModel(AsyncAttrs, DeclarativeBase, MappedAsDataclass):
    async def save_in_database(self, session: AsyncSession):
        session.add(self)
        await session.flush()

