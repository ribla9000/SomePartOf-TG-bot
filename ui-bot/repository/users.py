from repository.db import DatabaseRepository
from repository.tools import get_values
from db.users import users, ROLES
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
    async def get_by_chat_id(chat_id: str):
        query = sqlalchemy.select(users).where(users.c.chat_id == chat_id)
        values = await DatabaseRepository.fetch_one(query)
        if get_values(values) is None:
            return []
        return get_values(values)

    @staticmethod
    async def get_by_id(id: int):
        query = users.select().where(users.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_users_by_role(role: str, page: int):
        roles = [ROLES["GUEST"], ROLES["USER"], ROLES["MANAGER"], ROLES["ADMIN"], ROLES["SUPERADMIN"]]
        from_role = roles.index(role)
        if from_role is None:
            return []
        roles = roles[from_role::]
        query = f"""SELECT * FROM users WHERE role = ANY(ARRAY{roles}) LIMIT 14 OFFSET {page * 14};"""
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def update_role(id: int, role: str):
        query = users.update().values(role=role).where(users.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result