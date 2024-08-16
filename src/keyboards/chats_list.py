from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.services.get_db import get_db


class RetrieveChatCallback(CallbackData, prefix='chat_retrieve'):
    id: int


class GetLogsCallback(CallbackData, prefix='chats_logs'):
    id: int | None = None


@get_db
async def get_show_chats_keyboard(user_id: int, db) -> InlineKeyboardMarkup:
    # db without typehint cuz circ import
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


def get_back_keyboard(chat_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Вернуться назад',
                callback_data=RetrieveChatCallback(id=chat_id).pack()
            )
        ],
    ])
