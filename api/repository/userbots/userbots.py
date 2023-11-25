from repository.db import DatabaseRepository
from repository.tools import get_values
from db.userbots import userbots, TYPES
from db.userbots_subscriptions import userbots_subscriptions
import sqlalchemy


class UserBotsRepository(DatabaseRepository):

    @staticmethod
    async def get_by_id(id: int):
        query = userbots.select().where(userbots.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_channel(channel_id: str):
        query = userbots.select().where(userbots.c.channel_id == channel_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def update(id: int, values: dict):
        query = userbots.update().values(values).where(userbots.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_all(page: int):
        query = (userbots.select()
                 .where(userbots.c.type == None, userbots.c.nickname != None)
                 .offset(page * 14)
                 .limit(14))
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_by_type(type: str):
        if type not in list(TYPES.values()):
            return []
        query = userbots.select().where(userbots.c.type == type)
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_free_watcher():
        query = (
            sqlalchemy.select(
                userbots,
                sqlalchemy.func.count(userbots_subscriptions.c.chat_id).label('subscription_count')
            )
            .outerjoin(
                userbots_subscriptions,
                userbots.c.id == userbots_subscriptions.c.userbot_id
            )
            .group_by(userbots.c.id)
            .order_by(sqlalchemy.asc('subscription_count'))
            .where(userbots.c.type == "watcher")
        )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)