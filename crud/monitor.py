from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.monitor import MonitorInDB


async def get_monitors(session: AsyncSession):
    stmt = select(MonitorInDB)
    return (await session.scalars(stmt)).all()


async def get_monitor(session: AsyncSession, monitor_id: int) -> MonitorInDB:
    stmt = select(MonitorInDB).where(MonitorInDB.id == monitor_id)
    return (await session.scalars(stmt)).one()


async def delete_monitor(session: AsyncSession, monitor: MonitorInDB):
    await session.delete(monitor)

