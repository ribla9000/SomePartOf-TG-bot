from repository.db import DatabaseRepository
from repository.tools import get_values
from db.links import links
import sqlalchemy


class LinksRepository(DatabaseRepository):

    @staticmethod
    async def create(link: dict):
        query = links.insert(link)
        result = await DatabaseRepository.execute(query)
        return result
