import sqlalchemy
from core.db import metadata


grouping = sqlalchemy.Table(
    "grouping",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, nullable=False)
)
