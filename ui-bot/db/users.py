import enum
import sqlalchemy
from core.db import metadata


ROLES = {
    #ribla9000
}

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("nickname", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("role", sqlalchemy.String, nullable=False, server_default=ROLES["GUEST"])
)
