import os
from db.external_channels import external_channels
import sqlalchemy
from core.db import metadata


competitor_channels = sqlalchemy.Table(
    "competitor_channels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column(
        "external_channel_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(external_channels.c.id, ondelete="CASCADE"),
        nullable=False
    ),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("link", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=False),
)

