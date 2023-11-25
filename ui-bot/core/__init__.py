from core.db import metadata, engine
from db.users import users
from db.links import links
from db.admin_bots import admin_bots
from db.external_channels import external_channels
from db.ad_purchases import ad_purchases
from db.contacts import contacts
from db.user_channels import user_channels
from db.messages import messages
from db.support_messages import support_messages
from db.competitor_channels import competitor_channels
from db.grouping import grouping
from db.userbots_subscriptions import userbots_subscriptions


metadata.reflect(bind=engine)
