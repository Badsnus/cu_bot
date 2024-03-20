from src.models import db_session_maker
from src.repo import DB


def get_db(func):
    async def wrapper(*args, **kwargs):
        async with db_session_maker() as session:
            return await func(*args, **kwargs, db=DB(session))

    return wrapper
