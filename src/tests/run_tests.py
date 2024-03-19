from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import load_test_database_url
from src.models import Base
from src.repo import DB


class Tester:

    def __init__(self):
        db_connection = load_test_database_url()

        db_engine = create_async_engine(url=db_connection, echo=True)
        async with db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self.db_session_maker = async_sessionmaker(db_engine, expire_on_commit=False)

    @staticmethod
    def db(func):
        def wrapper(*args, **kwargs):
            self: Tester = args[0]
            async with self.db_session_maker() as session:
                return func(*args, **kwargs, db=DB(session))

        return wrapper
    # @db
    # def test_(self):
