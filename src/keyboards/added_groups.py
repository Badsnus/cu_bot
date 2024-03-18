from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.models import Chat
from src.repo import DB


class RetrieveGroupCallback(CallbackData, prefix='group_retrieve'):
    id: int


class GetLogsCallback(CallbackData, prefix='group_logs'):
    id: int = -1


async def get_show_groups_keyboard(user_id: int, db: DB) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    chats = await db.chat.get_chats_by_user(user_id)
    for chat in chats:
        builder.row(
            InlineKeyboardButton(text=chat.chat_name, callback_data=RetrieveGroupCallback(id=chat.telegram_id).pack()),
        )
    builder.row(InlineKeyboardButton(text='Выгрузить все логи', callback_data=GetLogsCallback().pack()))
    return builder.as_markup()


class ChangeModerLevelCallback(CallbackData, prefix='change_moder_level'):
    id: int


async def get_retrieve_keyboard(chat: Chat) -> InlineKeyboardMarkup:
    toggle_text = 'Выключить модерацию' if chat.moderation_level != 0 else 'Включить модерацию'
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=toggle_text,
                                 callback_data=ChangeModerLevelCallback(id=chat.telegram_id).pack()),
        ],
        [
            InlineKeyboardButton(text='Выгрузить логи', callback_data=GetLogsCallback(id=chat.telegram_id).pack()),
        ]
    ])
