from src.repo import DB
from src.services.get_db import get_db


@get_db
async def check_can_user_join(chat_id: int,
                              is_chat: bool,
                              username: str,
                              telegram_id: int,
                              db: DB) -> bool:
    if is_chat:
        chat = await db.chat.get(chat_id)
    else:
        chat = await db.chat.get_by_channel_id(chat_id)

    if not chat.is_white_list_on:
        return True

    white_list = await db.white_list.get_user_in_white_list(
        chat.telegram_id,
        username,
    )
    if not white_list:
        return False

    if white_list.telegram_id is None:
        white_list = await db.white_list.update(white_list, telegram_id)

    return white_list.telegram_id == telegram_id
