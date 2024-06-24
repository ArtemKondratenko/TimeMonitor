import asyncio
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from model.monitor import CreateMonitor
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from model.monitor import MonitorInDB, Monitor, UpdateMonitor
from executingRequests import launch_monitor
from background_tasks import  background_tasks
from  crud.monitor import get_monitor, get_monitors
from model.request import Request, RequestInDB
from crud.request import get_monitor_request
from urllib.parse import urlparse


monitor_router = APIRouter()

@monitor_router.post("/monitors")
async def create_monitor(
        monitor_data: CreateMonitor,
        session: Annotated[AsyncSession, Depends(get_session)]) -> Monitor:
    monitorInDB = MonitorInDB(url=monitor_data.url, email=monitor_data.email, interval=monitor_data.interval, tg_api_token=monitor_data.tg_api_token, tg_chat_id=monitor_data.tg_chat_id)
    await monitorInDB.save_in_database(session)
    task = asyncio.create_task(launch_monitor(monitorInDB.id))
    background_tasks[monitorInDB.id] = task
    return Monitor.model_validate(monitorInDB)

@monitor_router.get('/monitors/{monitor_id}')
async def monitor(
        monitor_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]) -> Monitor | None:
     monitor = await get_monitor(session, monitor_id)
     if not monitor:
         raise HTTPException(404)
     return Monitor.model_validate(monitor)

@monitor_router.get("/monitors")
async def monitors(
        session: Annotated[AsyncSession, Depends(get_session)]) -> list[Monitor]:
    monitors = await get_monitors(session)
    if not monitors:
        raise HTTPException(404)
    return  [Monitor.model_validate(monitor) for monitor in monitors]



@monitor_router.delete("/monitors/{monitor_id}")
async def delete_monitor(
        monitor_id: int,
        session: Annotated[AsyncSession,Depends(get_session)]):
    monitor = await get_monitor(session, monitor_id)
    task = background_tasks[monitor.id]
    if not monitor:
        raise HTTPException(404)
    task.cancel()
    del background_tasks[monitor.id]
    await session.delete(monitor)
    await  session.commit()


@monitor_router.put("/monitors/{monitor_id}")
async def put_monitor(
        monitor_id: int,
        monitor_data: UpdateMonitor,
        session: Annotated[AsyncSession, Depends(get_session)]) -> Monitor:
    monitor = await get_monitor(session, monitor_id)
    if not monitor:
        raise HTTPException(404)

    url = monitor_data.url or monitor.url
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f"http://{url}"
        monitor_data.url = url

    monitor.url = url
    monitor.interval = monitor_data.interval or monitor.interval
    if monitor_data.is_pause is not None:
        monitor.is_pause = monitor_data.is_pause
    monitor.email = monitor_data.email or monitor.email

    return monitor


@monitor_router.get("/monitors/{monitor_id}/requests")
async def request_monitor(
        monitor_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]) -> list[Request] | None:
    requests = await get_monitor_request(session, monitor_id)
    if requests is None:
        return None
    return [Request.model_validate(request) for request in requests]




