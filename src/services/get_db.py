from src.repo import DB


async def get_db() -> DB:
    # velosiped
    from bot import db_session_maker

    async with db_session_maker() as session:
        return DB(session)
