import sqlalchemy
from core.db import metadata


links = sqlalchemy.Table(
    "links",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    #ribla9000
)
