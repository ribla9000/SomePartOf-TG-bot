import sqlalchemy
from core.db import metadata


userbots_subscriptions = sqlalchemy.Table(
    "userbots_subscriptions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("chat_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("userbot_id", sqlalchemy.Integer, nullable=False),
)
