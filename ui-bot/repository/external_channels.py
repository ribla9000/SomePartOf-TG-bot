from repository.db import DatabaseRepository
from repository.tools import get_values
from db.external_channels import external_channels
from db.competitor_channels import competitor_channels
from db.grouping import grouping
import sqlalchemy
import datetime


class ExternalChannelsRepository(DatabaseRepository):

    @staticmethod
    async def create(channel: dict):
        query = external_channels.insert().values(channel)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_all_by_user(user_id: int, page: int, by_page: bool = True):
        now = datetime.datetime.now()
        query = (external_channels
                 .select()
                 .order_by(sqlalchemy.desc(external_channels.c.id))
                 .where(external_channels.c.user_id == user_id)
                 .limit(14)
                 .offset(page * 14))
        if not by_page:
            query = (external_channels
                     .select()
                     .order_by(sqlalchemy.desc(external_channels.c.id))
                     .where(external_channels.c.user_id == user_id))
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_by_id(id: int):
        query = external_channels.select().where(external_channels.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_info_to_user(ex_channel_id: int):
        query = (sqlalchemy
                 .select(competitor_channels.c.id,
                         competitor_channels.c.title,
                         competitor_channels.c.link,
                         competitor_channels.c.description)
                 .where(competitor_channels.c.external_channel_id == ex_channel_id))
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_info_by_id(id: int):
        query = (sqlalchemy
                 .select(competitor_channels.c.id,
                         competitor_channels.c.title,
                         competitor_channels.c.link,
                         competitor_channels.c.description)
                 .where(competitor_channels.c.id == id)
                 )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def delete(id: int):
        query = external_channels.delete().where(external_channels.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def update_grouping(channel_id: int, grouping_id: int, append: bool):
        query = f"""UPDATE external_channels SET group_ids = array_remove(group_ids, {grouping_id}) WHERE id = {channel_id};"""
        if append:
            query = f"""UPDATE external_channels SET group_ids = array_append(group_ids, {grouping_id}) WHERE id = {channel_id};"""

        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_grouping(grouping_id: int):
        query = f"""SELECT * FROM external_channels WHERE {grouping_id} = ANY(group_ids);"""
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

