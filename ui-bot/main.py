import os
from core.config import BOT_TOKEN, WEBHOOK_URL, SENTRY_TOKEN, ENVIRONMENT
from telegram import Update, Bot
import uvicorn
import sentry_sdk
from endpoints import ui_menu
from starlette.requests import Request
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route
from core.db import database
import asyncio
from telegram.ext import (
    Application,
    CommandHandler,
)


sentry_sdk.init(
    dsn=SENTRY_TOKEN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=ENVIRONMENT
)


async def bot_startup_webhook():

    async def start_hooking(request: Request):
        await application.update_queue.put(
            Update.de_json(data=await request.json(), bot=application.bot)
        )
        return Response()

    application = Application.builder().token(BOT_TOKEN).updater(None).build()
    ui_menu.add_handlers(application)
    await application.bot.set_webhook(url=WEBHOOK_URL, allowed_updates=Update.ALL_TYPES)
    starlette_app = Starlette(
        routes=[
            Route(f"/webhooks/", start_hooking, methods=["POST"]),
        ]
    )

    webserver = uvicorn.Server(
        config=uvicorn.Config(
            app=starlette_app,
            reload=True,
            port=8443,
            use_colors=True,
            host="0.0.0.0",
        )
    )

    async with application:
        await application.start()
        await webserver.serve()
        await application.stop()


async def db_startup():
    await database.connect()


def bot_startup_polling():
    application = Application.builder().token(BOT_TOKEN).build()
    ui_menu.add_handlers(application)
    loop = asyncio.get_event_loop()
    loop.create_task(db_startup())
    loop.create_task(application.run_polling(allowed_updates=Update.ALL_TYPES))


async def main():
    await db_startup()
    await bot_startup_webhook()


if __name__ == "__main__":
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    if ENVIRONMENT == "development":
        bot_startup_polling()
    else:
        asyncio.run(main())
