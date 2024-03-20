from src.models import db_session_maker
from src.repo import DB


async def get_db() -> DB:
    async with db_session_maker() as session:
        # sometimes warnings mb need to fix if data will lose
        return DB(session)
