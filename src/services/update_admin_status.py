from aiogram.enums import ChatMemberStatus

from src.services.get_db import get_db


async def update_admin_status(user_id: int,
                              chat_id: int,
                              old_status: str,
                              new_status: str) -> None:
    db = await get_db()

    mem = ChatMemberStatus.MEMBER
    adm = ChatMemberStatus.ADMINISTRATOR

    if old_status == mem and new_status == adm:
        await db.chat.add_admin(user_id, chat_id)

    elif old_status == adm and new_status != adm:
        await db.chat.delete_admin(user_id, chat_id)
