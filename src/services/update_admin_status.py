from aiogram.enums import ChatMemberStatus

from src.repo import DB


async def update_admin_status(user_id: int,
                              chat_id: int,
                              old_status: str,
                              new_status: str,
                              db: DB) -> None:
    if old_status == ChatMemberStatus.MEMBER and new_status == ChatMemberStatus.ADMINISTRATOR:
        await db.chat.add_admin(user_id, chat_id)

    elif old_status == ChatMemberStatus.ADMINISTRATOR and new_status != ChatMemberStatus.ADMINISTRATOR:
        await db.chat.delete_admin(user_id, chat_id)
