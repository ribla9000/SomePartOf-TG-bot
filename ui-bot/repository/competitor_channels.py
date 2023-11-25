from repository.db import DatabaseRepository
from repository.tools import get_values
from db.external_channels import external_channels
from db.competitor_channels import competitor_channels
import sqlalchemy


class CompetitorChannelsRepository:

    @staticmethod
    async def delete_all(open_link: str, user_id: int):
        query = competitor_channels.delete().where(
            external_channels.c.open_link == open_link,
            external_channels.c.user_id == user_id,
            competitor_channels.c.external_channel_id == external_channels.c.id
        )
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_count_by_title(title: str):
        query = competitor_channels.select().where(competitor_channels.c.title == title)
        result = await DatabaseRepository.fetch_all(query)
        return len(get_values(result))

    @staticmethod
    async def get_by_external_channel():
        pass
