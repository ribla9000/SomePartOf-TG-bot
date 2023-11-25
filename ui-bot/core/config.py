import os
import redis
from dotenv import load_dotenv

load_dotenv(".env")

REDIS_HOST = os.getenv("ENV_REDIS_HOST")
REDIS_PORT = os.getenv("ENV_REDIS_PORT")

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
redis_db = redis.Redis(connection_pool=pool)

#ribla9000
#ribla9000
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
API_BASE_URL = os.getenv("#ribla9000")
SENTRY_TOKEN = os.getenv("#ribla9000")
WEBHOOK_URL = os.getenv("#ribla9000")
ENVIRONMENT = os.getenv("ENVIRONMENT")

START_MENU = ["SETTINGS", "COMPETITOR", "SUPERADMIN", "STATISTICS"]
SETTINGS = ["SETTINGS_BACK", "BOTS", "CHANNELS", "AUTOCOMMENT", "AUTOLIKE", "SUPPORT"]
BOTS = ["BOTS_BACK", "ADD_BOT", "LIST_BOTS", "BOTS_CHOICE"]
CHANNELS = ["CHANNELS_BACK", "ADD_CHANNEL", "LIST_CHANNELS",
            "CHANNELS_AUTOCOMMENT", "CHANNELS_AUTOLIKE"]
USERBOTS = ["USERBOTS_BACK", "ADD_USERBOT", "LIST_USERBOTS"]
AUTOCOMMENT = ["AUTOCOMMENT_CHANNELS", "AUTOCOMMENT_STATUS", "AUTOCOMMENT_SETTINGS"]
SUPPORT = ["get_support_messages", "LEAVE_MESSAGE"]
BACK_BUTTON_TEXT = "«Back"

RESPONSE_ERROR = "ERROR"
RESPONSE_DONE = "Done"

SUPERADMIN_IDS = os.getenv("#ribla9000").split(',')
NOT_APPROVE = ("This bot requires manual approval in order to unlock advanced features. "
               "If you got here by accident - bye, if no - please contact  and send them this code:")
