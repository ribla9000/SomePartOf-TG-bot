import sqlalchemy
from core.db import metadata
from db.external_channels import external_channels
from db.links import links


ad_purchases = sqlalchemy.Table(
    "ad_purchases",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    #ribla9000
)
