from repository.db import DatabaseRepository
from repository.tools import get_values
from db.userbots import userbots
from db.userbots_subscriptions import userbots_subscriptions
import sqlalchemy


class UserbotsSubscriptionsRepository(DatabaseRepository):

    @staticmethod
    async def create(subscription: dict):
        query = userbots_subscriptions.insert().values(subscription)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_userbot(chat_id: str):
        query = (sqlalchemy.select(userbots)
                 .where(userbots_subscriptions.c.chat_id == chat_id,
                        userbots.c.id == userbots_subscriptions.c.userbot_id))
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def is_subscribed(userbot_id: int, chat_id: str):
        query = (sqlalchemy.select(userbots)
                 .where(userbots_subscriptions.c.userbot_id == userbot_id, userbots_subscriptions.c.chat_id == chat_id))
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)
