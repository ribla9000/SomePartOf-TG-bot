import sqlalchemy
from core.db import metadata


messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("message", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("query", sqlalchemy.String, nullable=True),
)