from repository.db import DatabaseRepository
from repository.tools import get_values
from db.user_channels import user_channels
from db.users import users
import sqlalchemy


class UserChannelsRepository(DatabaseRepository):

    @staticmethod
    async def create(channel: dict):
        query = user_channels.insert().values(channel)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_chat_id(chat_id: str, user_id):
        query = user_channels.select().where(user_channels.c.chat_id == chat_id, user_channels.c.user_id == user_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_all(id: str):
        query = (sqlalchemy
                 .select(user_channels)
                 .where(users.c.id == id,
                        user_channels.c.user_id == users.c.id,
                        user_channels.c.is_shown == True,
                        user_channels.c.admin_bot_id is not None)
                 )
        values = await DatabaseRepository.fetch_all(query)
        return get_values(values)

    @staticmethod
    async def update_admin_bot_id(id: int, bot_id):
        query = user_channels.update().where(user_channels.c.id == id).values(admin_bot_id=bot_id)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_id(id: int):
        query = user_channels.select().where(user_channels.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def update_is_active(id: int, status: bool):
        query = user_channels.update().where(user_channels.c.id == id).values(is_active=status)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def delete(id: int):
        query = user_channels.delete().where(user_channels.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result
