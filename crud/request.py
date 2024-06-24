from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.request import RequestInDB




async def get_monitor_request(session: AsyncSession, monitor_id: int):
    stmt = select(RequestInDB).where(RequestInDB.monitor_id == monitor_id)
    return (await session.scalars(stmt)).all()
