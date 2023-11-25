import sqlalchemy
from core.db import metadata


user_channels_users = sqlalchemy.Table(
    "user_channels_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("nickname", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.String, nullable=False),
)
