from src.models import User
from src.repo import DB


async def get_or_create_user(user_id: int, db: DB) -> User:
    user = await db.user.get(telegram_id=user_id)
    if user:
        return user
    return await db.user.create(user_id)
