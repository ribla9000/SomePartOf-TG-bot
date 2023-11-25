from repository.db import DatabaseRepository
from repository.tools import get_values
from db.users import users
import sqlalchemy


class UsersRepository(DatabaseRepository):

    @staticmethod
    async def create(user: dict):
        query = users.insert(user)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_all():
        query = users.select()
        values = await DatabaseRepository.fetch_all(query)
        return get_values(values)

    @staticmethod
    async def get_by_nickname(nickname: str):
        query = sqlalchemy.select(users.c.id).where(users.c.nickname == nickname)
        values = await DatabaseRepository.fetch_one(query)
        if get_values(values) is None:
            return None
        return get_values(values) if len(values) > 0 else None