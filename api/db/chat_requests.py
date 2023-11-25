import sqlalchemy
from core.db import metadata


chat_requests = sqlalchemy.Table(
    "chat_requests",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_channel_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("user_channel_user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("invite_link", sqlalchemy.String, nullable=True),
)
