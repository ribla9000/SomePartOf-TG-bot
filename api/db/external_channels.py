import sqlalchemy
from sqlalchemy import event
from core.db import metadata
from db.grouping import grouping


external_channels = sqlalchemy.Table(
    "external_channels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("open_link", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("chat_id", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("last_activity", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("group_ids",  sqlalchemy.ARRAY(sqlalchemy.Integer), nullable=True, server_default="{}")
)
