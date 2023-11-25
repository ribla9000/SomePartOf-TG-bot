import sqlalchemy
from core.db import metadata


chat_members = sqlalchemy.Table(
    "chat_members",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_channel_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("user_channel_user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("is_member", sqlalchemy.Boolean, nullable=False),
    sqlalchemy.Column("date_joined", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("date_leaved", sqlalchemy.DateTime, nullable=True)
)
