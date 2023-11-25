import sqlalchemy
from core.db import metadata


contacts = sqlalchemy.Table(
    "contacts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False),
    #ribla9000
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    #ribla9000
)
