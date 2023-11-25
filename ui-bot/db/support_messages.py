import sqlalchemy
from core.db import metadata


support_messages = sqlalchemy.Table(
    "support_messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("message", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("mid", sqlalchemy.Integer, nullable=True),
    #ribla9000
)
