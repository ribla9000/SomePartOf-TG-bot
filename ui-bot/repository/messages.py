from repository.db import DatabaseRepository
from repository.tools import get_values
from db.users import users
from db.messages import messages
import sqlalchemy


class MessagesRepository(DatabaseRepository):

    @staticmethod
    async def create(message: dict):
        query = messages.insert().values(message)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_last(nickname: str):
        query = (sqlalchemy.select(messages)
                 .order_by(sqlalchemy.desc(messages.c.id))
                 .where(users.c.nickname == nickname,
                        users.c.id == messages.c.user_id)
                 )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def update(id: int, message: str):
        query = messages.update().where(messages.c.id == id).values(message=message)
        result = await DatabaseRepository.execute(query)
        return result