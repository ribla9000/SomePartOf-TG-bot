from repository.db import DatabaseRepository
from db.chat_members import chat_members
from repository.tools import get_values


class ChatMembersRepository(DatabaseRepository):

    @staticmethod
    async def create(values: dict):
        query = chat_members.insert().values(values)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_ids(user_id: int, channel_id: int):
        query = chat_members.select().where(
            chat_members.c.user_channel_id == channel_id,
            chat_members.c.user_channel_user_id == user_id
        )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def update(id: int, values: dict):
        query = chat_members.update().values(values).where(chat_members.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result
