from repository.db import DatabaseRepository
from repository.tools import get_values
from db.admin_bots import admin_bots
from db.user_channels import user_channels
from db.users import users
import sqlalchemy


class AdminBotsRepository(DatabaseRepository):

    @staticmethod
    async def create(admin_bot: dict):
        query = admin_bots.insert(admin_bot)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_all(user_id: int):
        query = (sqlalchemy.select(admin_bots)
                 .where(users.c.id == user_id,
                        admin_bots.c.user_id == users.c.id)
                 )
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_by_channel_id(channel_id: int):
        query = admin_bots.select().where(user_channels.c.id == channel_id,
                                          user_channels.c.admin_bot_id == admin_bots.c.id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

