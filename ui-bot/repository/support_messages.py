from repository.db import DatabaseRepository
from repository.tools import get_values
from db.support_messages import support_messages
from db.users import users
import sqlalchemy


class SupportMessagesRepository(DatabaseRepository):

    @staticmethod
    async def get_users():
        query = (sqlalchemy.select(support_messages.c.id, users.c.nickname, users.c.chat_id)
                 .where(support_messages.c.is_reply == False,
                        support_messages.c.is_answered == False,
                        support_messages.c.user_id == users.c.id))
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def create(message: dict):
        query = support_messages.insert().values(message)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_id(id: int):
        query = support_messages.select().where(support_messages.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_last_by_supporter(nickname: str):
        query = #ribla9000
        return get_values(result)

    @staticmethod
    async def update(id: int, message: dict):
        query = support_messages.update().where(support_messages.c.id == id).values(message)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def make_answered(mid: int, chat_id: str):
        #ribla9000
        return result
