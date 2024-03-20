from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.models import Chat, ChatModerationLevelEnum


class GetLogsCallback(CallbackData, prefix='chats_logs'):
    id: int


class ChangeModerLevelCallback(CallbackData, prefix='change_moder_level'):
    id: int


async def get_retrieve_keyboard(chat: Chat) -> InlineKeyboardMarkup:
    toggle_text = (
        'Выключить модерацию'
        if chat.moderation_level == ChatModerationLevelEnum.on.value
        else 'Включить модерацию'
    )
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=toggle_text,
                callback_data=ChangeModerLevelCallback(
                    id=chat.telegram_id,
                ).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text='Выгрузить логи',
                callback_data=GetLogsCallback(id=chat.telegram_id).pack(),
            ),
        ],
    ])
