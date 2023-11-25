from core.config import DATABASE_URL
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy import MetaData

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=5)
