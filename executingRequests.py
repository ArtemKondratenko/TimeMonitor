import asyncio
from datetime import timedelta
import time

import httpx

from database import get_session_in_context
from crud.monitor import get_monitor
from model.monitor import MonitorInDB
from sqlalchemy.ext.asyncio import AsyncSession
from background_tasks import background_tasks
from sending_notification import message_tg_bot
from model.request import RequestInDB

# TG_API_TOKEN = "7290146360:AAHOftbFDEgREERHS3YdCLlAVatc1lKxxNA"
# TG_CHAT_ID = 216186488

async def monitor_url(
    monitor: MonitorInDB,
    session: AsyncSession,
):
    try:
        async with httpx.AsyncClient() as client:
            start = time.time()
            response = await client.get(monitor.url)
            status_code = response.status_code
            if status_code != 200:
                if monitor.id in background_tasks:
                    background_tasks[monitor.id].cancel()
                await message_tg_bot(monitor.tg_api_token, monitor.tg_chat_id, monitor, status_code)
            end = time.time()
            response_time = end - start
            time_delta = timedelta(seconds=response_time)
            request_in_db = RequestInDB(
                url=monitor.url,
                time=time_delta,
                status_code=status_code,
                monitor_id=monitor.id
            )
            await request_in_db.save_in_database(session)
    except:
        pass


async def launch_monitor(monitor_id: int):
    while True:
        async with get_session_in_context() as session:
            monitor = await get_monitor(session, monitor_id)
            if not monitor:
                break
            await monitor_url(monitor, session)
            interval_in_seconds=monitor.interval.total_seconds()
        await asyncio.sleep(interval_in_seconds)