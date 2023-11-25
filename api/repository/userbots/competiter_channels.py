import datetime
from repository.db import DatabaseRepository
from repository.tools import get_values
from db.competitor_channels import competitor_channels
from db.external_channels import external_channels
import sqlalchemy


class CompetitorChannelsRepository(DatabaseRepository):

    @staticmethod
    async def create(channel: dict):
        query = competitor_channels.insert().values(channel)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_url(url: str):
        query = (sqlalchemy.select(competitor_channels, external_channels.c.last_activity)
                 .order_by(sqlalchemy.desc(competitor_channels.c.id))
                 .where(competitor_channels.c.link == url)
                 )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_last_result(external_channel_id: int, parsed_time_delta_hours: int):
        query = (sqlalchemy.select(competitor_channels)
        .order_by(sqlalchemy.asc(competitor_channels.c.id))
        .where(
            external_channels.c.id == external_channel_id,
            competitor_channels.c.external_channel_id == external_channel_id,
            datetime.datetime.now() - external_channels.c.last_activity < datetime.timedelta(
                hours=parsed_time_delta_hours))
        )

        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_user_channel(external_id: int, title: str):
        query = (sqlalchemy.select(competitor_channels)
                 .where(competitor_channels.c.external_channel_id == external_id,
                        competitor_channels.c.title == title)
                 )
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_result_by_chat_id(chat_id: str):
        query = (sqlalchemy.select(#ribla9000)
                 .order_by(sqlalchemy.asc(competitor_channels.c.id))
                 .where(external_channels.c.chat_id == chat_id,
                        competitor_channels.c.external_channel_id == external_channels.c.id)
                 )
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

    @staticmethod
    async def get_count(url: str):
        query = sqlalchemy.select(sqlalchemy.func.count(competitor_channels.c.id)).where(competitor_channels.c.link == url)
        result = await DatabaseRepository.fetch_all(query)
        return get_values(result)

