from src.models import db_session_maker
from src.repo import DB


async def get_db() -> DB:
    async with db_session_maker() as session:
        return DB(session)
