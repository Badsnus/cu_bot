from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from config import load_config

Base = declarative_base()

db_engine = create_async_engine(url=load_config().db_connection)
db_session_maker = async_sessionmaker(db_engine, expire_on_commit=False)
