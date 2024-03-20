from datetime import datetime

from .get_db import get_db


async def create_bad_message_log(chat_id: int,
                                 chat_name: str,
                                 user_name: str,
                                 user_id: int,
                                 time: datetime,
                                 text: str,
                                 is_from_bot) -> None:
    db = await get_db()
    await db.log.create(
        chat_id=chat_id,
        user_id=user_id,
        message='[SERVICE] bot payment' if is_from_bot else text,
        time=time,
        chat_name=chat_name,
        user_name=user_name,
    )
