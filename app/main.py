import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.config import APP_TITLE, APP_VERSION
from app.db.pool import create_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_pool()
    app.state.graph, app.state.lock = None, asyncio.Lock()
    yield
    await app.state.pool.close()

def create_app() -> FastAPI:
    application = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)
    application.include_router(api_router)
    return application

app = create_app()
