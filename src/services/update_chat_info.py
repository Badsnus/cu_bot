from typing import Callable

from aiogram.types import ChatMemberAdministrator

from src.models import Chat
from src.repo import DB
from src.services.get_db import get_db


@get_db
async def update_chat_info(chat_id: int,
                           chat_name: str,
                           get_admins_method: Callable,
                           bot_id: int,
                           db: DB,
                           from_user_id: int = 0,
                           sender_chat_id: int | None = None,
                           ) -> Chat:
    chat = await db.chat.get(chat_id)
    if chat is None:
        chat = await db.chat.create(
            telegram_id=chat_id, chat_name=chat_name,
            channel_telegram_id=(
                from_user_id == 777000 and sender_chat_id or None
            ),
        )

        admins: list[ChatMemberAdministrator] = (
            await get_admins_method(chat_id)
        )
        await db.chat.add_admins(admins, chat_id, bot_id)

    channel_telegram_id = chat.channel_telegram_id
    if from_user_id == 777000 and sender_chat_id:
        channel_telegram_id = sender_chat_id

    await db.chat.update_name_and_telegram_channel_id(
        chat,
        chat_name,
        channel_telegram_id,
    )

    return chat
