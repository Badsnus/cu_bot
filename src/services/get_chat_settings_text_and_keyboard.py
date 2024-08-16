from aiogram.types import InlineKeyboardMarkup

from src.keyboards.chat_retrieve import get_retrieve_keyboard
from src.models import Chat
from src.repo import DB
from src.services.get_db import get_db


class ChatSettingsView:
    bot_link = 'BUGGGGG'

    def __init__(self, chat_id: int) -> None:
        self._chat_id = chat_id

    async def _get_text_and_keyboard(
            self,
            chat: Chat) -> tuple[str, InlineKeyboardMarkup]:
        return (
            f'Чат: <b>{chat.chat_name}\n</b>'
            f'Статус модерирования: <b>{chat.moderation_level}</b>\n'
            f'Канал: <b>{chat.channel_telegram_id or "❌"}</b>\n'
            f'Ссылка на вступление: \n'
            f'https://t.me/{self.bot_link}?start={chat.invite_code}',
            await get_retrieve_keyboard(chat)
        )

    @get_db
    async def get(self, db: DB) -> tuple[str, InlineKeyboardMarkup]:
        chat = await db.chat.get(self._chat_id)
        return await self._get_text_and_keyboard(chat)

    @get_db
    async def update_moder_level(
            self,
            db: DB) -> tuple[str, InlineKeyboardMarkup]:
        chat = await db.chat.update_moder_level(self._chat_id)
        return await self._get_text_and_keyboard(chat)

    @get_db
    async def update_white_list_status(
            self,
            db: DB) -> tuple[str, InlineKeyboardMarkup]:
        chat = await db.chat.update_white_list_status(self._chat_id)
        return await self._get_text_and_keyboard(chat)
