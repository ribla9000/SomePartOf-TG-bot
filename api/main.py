from fastapi import FastAPI, Request
from endpoints import watcher_bots, admin_bots, userbots, statbots, user_channels
from core.db import database
from core.config import SENTRY_TOKEN, ENVIRONMENT
from alembic.config import Config
from alembic import command
import uvicorn
import logging
import sentry_sdk

sentry_sdk.init(
    dsn=SENTRY_TOKEN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=ENVIRONMENT
)

app = FastAPI(title="Auto API")
app.include_router(watcher_bots.router, prefix="/watchers", tags=["watchers"])
app.include_router(admin_bots.router, prefix="/admin-bots", tags=["admin-bots"])
app.include_router(userbots.router, prefix="/userbots", tags=["userbots"])
app.include_router(statbots.router, prefix="/stats", tags=["stats"])
app.include_router(user_channels.router, prefix="/user-channels", tags=["user-channels"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    alembic_cfg = Config("./alembic.ini")
    command.upgrade(alembic_cfg, "head")
    uvicorn.run("main:app",
                port=8000,
                host="0.0.0.0",
                reload=True)
