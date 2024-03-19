from aiogram.types import InlineKeyboardMarkup

from src.keyboards.chats import get_retrieve_keyboard
from src.repo import DB


async def get_chat_settings_text_and_keyboard(chat_id: int,
                                              db: DB) -> tuple[str, InlineKeyboardMarkup]:
    chat = await db.chat.get_by_tg_id(chat_id)

    return (
        f'Чат {chat.chat_name}\n'
        f'Статус модерирования {chat.moderation_level}',
        await get_retrieve_keyboard(chat)
    )
