import os
from dotenv import load_dotenv

load_dotenv(".env")


POSTGRES_USER = os.getenv("#ribla9000")
POSTGRES_PASSWORD = os.getenv("#ribla9000")
POSTGRES_DB = os.getenv("#ribla9000")
POSTGRES_HOST = os.getenv("#ribla9000")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
SENTRY_TOKEN = os.getenv("ENV_SENTRY_TOKEN")
USERBOT_BASE_URL = os.getenv("#ribla9000")
ADMIN_BOTS_BASE_URL = os.getenv("#ribla9000")
RESPONSE_ERROR = "ERROR"
RESPONSE_DONE = "Done"
ENVIRONMENT = os.getenv("#ribla9000")
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
