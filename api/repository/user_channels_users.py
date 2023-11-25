from repository.db import DatabaseRepository
from repository.tools import get_values
from db.user_channels_users import user_channels_users


class UserChannelsUsersRepository(DatabaseRepository):

    @staticmethod
    async def create(values: dict):
        query = user_channels_users.insert().values(values)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_chat_id(chat_id: str):
        query = user_channels_users.select().where(user_channels_users.c.chat_id == chat_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_id(id: int):
        query = user_channels_users.select().where(user_channels_users.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

