import sqlalchemy
from core.db import metadata


user_channels = sqlalchemy.Table(
    "user_channels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    #ribla9000
)
