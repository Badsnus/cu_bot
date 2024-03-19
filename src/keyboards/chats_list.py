from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.repo import DB


class RetrieveChatCallback(CallbackData, prefix='chat_retrieve'):
    id: int


class GetLogsCallback(CallbackData, prefix='chats_logs'):
    id: int | None = None


async def get_show_chats_keyboard(user_id: int,
                                  db: DB) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    chats = await db.chat.get_chats_by_user(user_id)
    for chat in chats:
        builder.row(
            InlineKeyboardButton(
                text=chat.chat_name,
                callback_data=RetrieveChatCallback(id=chat.telegram_id).pack(),
            ),
        )
    builder.row(
        InlineKeyboardButton(
            text='Выгрузить все логи',
            callback_data=GetLogsCallback().pack(),
        ),
    )
    return builder.as_markup()
