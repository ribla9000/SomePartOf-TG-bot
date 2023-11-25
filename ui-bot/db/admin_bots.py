import sqlalchemy
from core.db import metadata


admin_bots = sqlalchemy.Table(
    "admin_bots",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    #ribla9000
)
