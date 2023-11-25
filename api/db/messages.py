import sqlalchemy
from core.db import metadata
from db.users import users
from db.admin_bots import admin_bots


messages = sqlalchemy.Table(
    "messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    #ribla9000
)
