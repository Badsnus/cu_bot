from src.models import User
from src.services.get_db import get_db


async def get_or_create_user(user_id: int) -> User:
    db = await get_db()

    user = await db.user.get(telegram_id=user_id)
    if user:
        return user
    return await db.user.create(user_id)
