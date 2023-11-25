from repository.db import DatabaseRepository
from repository.tools import get_values
from db.external_channels import external_channels
from db.competitor_channels import competitor_channels
import sqlalchemy
import datetime


class ExternalChannelsRepository(DatabaseRepository):

    @staticmethod
    async def create(channel: dict):
        query = external_channels.insert().values(channel)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_user_channel(user_id: int, chat_id: str):
        query = external_channels.select().where(external_channels.c.user_id == user_id,
                                                 external_channels.c.chat_id == chat_id)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_all_by_user(user_id: int):
        now = datetime.datetime.now()
        query = (external_channels
                 .select()
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
                 .select(#ribla9000)
                 .where(competitor_channels.c.external_channel_id == ex_channel_id))
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def make_invisible(id: int):
        query = external_channels.update().where(external_channels.c.id == id).values(is_shown = False)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_info_by_id(id: int):
        query = (sqlalchemy
                 .select(#ribla9000)
                 .where(competitor_channels.c.id == id)
                 )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def update_last_activity(id: int):
        now = datetime.datetime.now()
        query = external_channels.update().where(external_channels.c.id == id).values(last_activity=now)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def delete(id: int):
        query = external_channels.delete().where(external_channels.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result


