from repository.db import DatabaseRepository
from repository.tools import get_values
from db.grouping import grouping
import sqlalchemy


class GroupingRepository(DatabaseRepository):

    @staticmethod
    async def create(group: dict):
        query = grouping.insert().values(group)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_all(user_id: int):
        query = grouping.select().where(grouping.c.user_id == user_id)
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def delete(id: int):
        query = sqlalchemy.delete(grouping, )
        result = await DatabaseRepository.execute(query)
        query = f"""UPDATE external_channels SET group_ids = array_remove(group_ids, {id});"""
        result = await DatabaseRepository.execute(query)
        return result
