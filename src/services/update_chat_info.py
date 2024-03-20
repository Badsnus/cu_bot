from aiogram.types import ChatMemberAdministrator

from src.models import Chat
from src.services.get_db import get_db


async def update_chat_info(chat_id: int,
                           chat_name: str,
                           admins: list[ChatMemberAdministrator],
                           bot_id: int) -> Chat:
    db = await get_db()

    chat = await db.chat.get(chat_id)
    if chat is None:
        chat = await db.chat.create(telegram_id=chat_id, chat_name=chat_name)
        await db.chat.add_admins(admins, chat_id, bot_id)

    await db.chat.update_name(chat, chat_name)

    return chat
