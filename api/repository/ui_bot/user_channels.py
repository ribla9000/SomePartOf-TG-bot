from repository.db import DatabaseRepository
from repository.tools import get_values
from db.user_channels import user_channels


class UserChannelsRepository(DatabaseRepository):

    @staticmethod
    async def create(channel: dict):
        query = user_channels.insert(channel)
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
    async def remove_admin_bot(id: int):
        query = user_channels.update().where(user_channels.c.id == id).values(admin_bot_id=None)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def update(id: int, values: dict):
        query = user_channels.update().where(user_channels.c.id == id).values(values)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_chat_id(chat_id: str):
        query = user_channels.select().where(user_channels.c.chat_id == chat_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)
