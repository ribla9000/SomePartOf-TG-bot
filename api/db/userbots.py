import sqlalchemy
from core.db import metadata


TYPES = {"WATCHER": "watcher", "WORKER": "worker"}


userbots = sqlalchemy.Table(
    "userbots",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("api_hash", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("api_id", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("session", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("type", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("phone_number", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("nickname", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=True),
)
