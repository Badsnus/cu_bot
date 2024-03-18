from aiogram import Bot
from aiogram.types import Message

from src.repo import DB


async def update_chat_info(message: Message, db: DB, bot: Bot) -> None:
    chat = await db.chat.get_by_tg_id(message.chat.id)
    if chat is None:
        chat = await db.chat.create(telegram_id=message.chat.id, chat_name=message.chat.title)

        admins = await bot.get_chat_administrators(chat_id=message.chat.id)
        await db.chat.add_admins(admins, message.chat.id, bot)

    await db.chat.update_name(chat, message.chat.title)
