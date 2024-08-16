import uuid

from aiogram import Bot

from src.repo import DB
from src.services.get_db import get_db


@get_db
async def check_access_to_chat(invite_code: str,
                               username: str,
                               bot: Bot,
                               db: DB) -> str:
    chat = await db.chat.get_by_invite_code(invite_code)

    if chat is None:
        return '<b>Чата с таким кодом не существует</b>\nЕсли вы думаете, что это ошибка - напишите @badsnus'

    is_in_white_list = await db.white_list.check_is_user_in_white_list(chat.telegram_id, username)

    if not is_in_white_list:
        return '<b>Вас нет в списке участников - напишите администратору</b>'

    chat_invite_link = await bot.create_chat_invite_link(
        chat.telegram_id,
        creates_join_request=True,
        name=username,
    )

    text = f'<b>{chat.chat_name}</b>\n\n<b>Ссылка на чат:</b> {chat_invite_link.invite_link}'
    if chat.channel_telegram_id:
        try:
            channel_invite_link = await bot.create_chat_invite_link(
                chat.channel_telegram_id,
                creates_join_request=True,
                name=username,
            )
            text += f'\n<b>Ссылка на канал:</b> {channel_invite_link.invite_link}'
        except:
            text += 'Доступ к каналу не настроен - сообщите об этом администратору'

    return text
