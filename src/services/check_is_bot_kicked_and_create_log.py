from datetime import datetime

from src.repo import DB
from src.services.create_service_notig_log import create_member_leave_log


async def check_is_bot_kicked_and_create_log(member_user_id: int,
                                             member_user_name: str,
                                             bot_id: int,
                                             chat_id: int,
                                             chat_name: str,
                                             message_time: datetime,
                                             from_user_id: int,
                                             from_user_username: str,
                                             db: DB) -> None:
    if member_user_id == bot_id:
        await db.chat.delete(chat_id)
        return

    await create_member_leave_log(
        chat_id=chat_id,
        chat_name=chat_name,
        message_time=message_time,
        member_user_id=member_user_id,
        member_user_name=member_user_name,
        from_user_id=from_user_id,
        from_user_username=from_user_username,
        db=db,
    )
