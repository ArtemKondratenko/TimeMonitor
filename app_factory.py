import asyncio
from contextlib import asynccontextmanager
from database import init_database, get_session_in_context
from fastapi import FastAPI
from crud.monitor import get_monitors
from executingRequests import launch_monitor
from background_tasks import background_tasks
from router.monitor import monitor_router







@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with get_session_in_context() as session:
        await init_database()
        monitors_id = [monitor.id for monitor in await get_monitors(session)]
    for id in monitors_id:
        task = asyncio.create_task(launch_monitor(id))
        background_tasks[id] = task
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(monitor_router)
    return app

