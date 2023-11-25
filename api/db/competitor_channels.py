from db.external_channels import external_channels
import sqlalchemy
from core.db import metadata


competitor_channels = sqlalchemy.Table(
    "competitor_channels",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column(
        "external_channel_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(external_channels.c.id, ondelete="CASCADE"),
        nullable=False
    ),
    #ribla9000
    sqlalchemy.Column("message_id", sqlalchemy.Integer, nullable=True)
)

