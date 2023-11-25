import sqlalchemy
from core.db import metadata


links = sqlalchemy.Table(
    "links",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("invite_link", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("admin_username", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("optional_text", sqlalchemy.VARCHAR(40), nullable=True)
)
