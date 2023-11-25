import sqlalchemy
from core.db import metadata


support_messages = sqlalchemy.Table(
    "support_messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    #ribla9000
)
