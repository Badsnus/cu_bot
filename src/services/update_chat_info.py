from aiogram import Bot
from aiogram.types import ChatMemberAdministrator, Message

from src.models import Chat
from src.repo import DB


async def update_chat_info(chat_id: int,
                           chat_name: str,
                           admins: list[ChatMemberAdministrator],
                           bot_id: int,
                           db: DB) -> Chat:
    chat = await db.chat.get_by_tg_id(chat_id)
    if chat is None:
        chat = await db.chat.create(telegram_id=chat_id, chat_name=chat_name)
        await db.chat.add_admins(admins, chat_id, bot_id)

    await db.chat.update_name(chat, chat_name)

    return chat
