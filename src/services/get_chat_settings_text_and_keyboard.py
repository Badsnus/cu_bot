from aiogram.types import InlineKeyboardMarkup

from src.keyboards.chat_retrieve import get_retrieve_keyboard
from src.models import Chat
from src.repo import DB


async def _get_text_and_keyboard(chat: Chat) -> tuple[str, InlineKeyboardMarkup]:
    return (
        f'Чат {chat.chat_name}\n'
        f'Статус модерирования {chat.moderation_level}',
        await get_retrieve_keyboard(chat)
    )


async def get_chat_settings_text_and_keyboard(chat_id: int,
                                              db: DB) -> tuple[str, InlineKeyboardMarkup]:
    chat = await db.chat.get_by_tg_id(chat_id)
    return await _get_text_and_keyboard(chat)


async def update_chat_settings_and_get_text_and_keyboard(chat_id: int,
                                                         db: DB) -> tuple[str, InlineKeyboardMarkup]:
    chat = await db.chat.update_moder_level(chat_id)
    return await _get_text_and_keyboard(chat)
