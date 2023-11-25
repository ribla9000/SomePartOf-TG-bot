from repository.db import DatabaseRepository
from repository.tools import get_values
from db.admin_bots import admin_bots
from db.user_channels import user_channels
import sqlalchemy


class AdminBotsRepository(DatabaseRepository):

    @staticmethod
    async def create(admin_bot: dict):
        query = admin_bots.insert().values(admin_bot)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_by_id(id: int):
        query = admin_bots.select().where(admin_bots.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_channel_id(channel_id: int):
        query = (admin_bots.select()
                 .where(user_channels.c.id == channel_id,
                        admin_bots.c.id == user_channels.c.admin_bot_id))
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_user(token: str, user_id: int):
        query = admin_bots.select().where(admin_bots.c.token == token, admin_bots.c.user_id == user_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)
