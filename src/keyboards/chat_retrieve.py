from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.models import Chat, ChatModerationLevelEnum


class GetLogsCallback(CallbackData, prefix='chats_logs'):
    id: int


class ChangeModerLevelCallback(CallbackData, prefix='change_moder_level'):
    id: int


class ToggleWhiteListCallback(CallbackData, prefix='toggle_white_list'):
    id: int


class GetWhiteListMembersCallback(CallbackData,
                                  prefix='get_white_list_members'):
    id: int


class ChangeWhiteListMemberCallback(CallbackData,
                                    prefix='add_white_list_member'):
    id: int
    is_add: bool


async def get_retrieve_keyboard(chat: Chat) -> InlineKeyboardMarkup:
    toggle_text = (
        'Выключить модерацию'
        if chat.moderation_level == ChatModerationLevelEnum.on.value
        else 'Включить модерацию'
    )
    if chat.is_white_list_on:
        buttons = [
            [
                InlineKeyboardButton(
                    text='Выключить white list',
                    callback_data=ToggleWhiteListCallback(
                        id=chat.telegram_id,
                    ).pack(),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Получить участников WL',
                    callback_data=GetWhiteListMembersCallback(
                        id=chat.telegram_id,
                    ).pack(),
                ),

            ],
            [
                InlineKeyboardButton(
                    text='Добавить юзеров в WL',
                    callback_data=ChangeWhiteListMemberCallback(
                        id=chat.telegram_id,
                        is_add=True,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text='Удалить юзеров в WL',
                    callback_data=ChangeWhiteListMemberCallback(
                        id=chat.telegram_id,
                        is_add=False,
                    ).pack(),
                ),
            ],
        ]
    else:
        buttons = [
            [
                InlineKeyboardButton(
                    text='Включить white list',
                    callback_data=ToggleWhiteListCallback(
                        id=chat.telegram_id,
                    ).pack(),
                ),
            ],
        ]

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=toggle_text,
                callback_data=ChangeModerLevelCallback(
                    id=chat.telegram_id,
                ).pack(),
            ),
        ],
        *buttons,
        [
            InlineKeyboardButton(
                text='Выгрузить логи',
                callback_data=GetLogsCallback(id=chat.telegram_id).pack(),
            ),
        ],
    ])
