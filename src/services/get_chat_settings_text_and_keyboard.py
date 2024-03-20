from aiogram.types import InlineKeyboardMarkup

from src.keyboards.chat_retrieve import get_retrieve_keyboard
from src.models import Chat
from src.services.get_db import get_db


class ChatSettingsView:

    def __init__(self, chat_id: int) -> None:
        self._chat_id = chat_id

    @staticmethod
    async def _get_text_and_keyboard(
            chat: Chat) -> tuple[str, InlineKeyboardMarkup]:
        return (
            f'Чат: <b>{chat.chat_name}\n</b>'
            f'Статус модерирования: <b>{chat.moderation_level}</b>',
            await get_retrieve_keyboard(chat)
        )

    async def get(self) -> tuple[str, InlineKeyboardMarkup]:
        db = await get_db()

        chat = await db.chat.get(self._chat_id)
        return await self._get_text_and_keyboard(chat)

    async def update(self) -> tuple[str, InlineKeyboardMarkup]:
        db = await get_db()

        chat = await db.chat.update_moder_level(self._chat_id)
        return await self._get_text_and_keyboard(chat)
