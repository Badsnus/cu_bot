import re
from datetime import datetime

from src.models import Chat, ChatModerationLevelEnum
from src.repo import DB

# todo офк надо отсюда вынести
bad_words = set(open('bad_words.txt', encoding='utf-8').read().splitlines())


def is_bad_text(text: str) -> bool:
    words = set(re.findall(r'\w+', text))
    return bool(words & bad_words)


async def create_bad_message_log(db: DB,
                                 chat_id: int,
                                 chat_name: str,
                                 user_name: str,
                                 user_id: int,
                                 time: datetime,
                                 text: str) -> None:
    await db.log.create(
        chat_id=chat_id,
        user_id=user_id,
        message=text,
        time=time,
        chat_name=chat_name,
        user_name=user_name,
    )


async def check_message_and_create_log_if_message_is_bad(
        chat_id: int,
        chat_name: str,
        user_name: str,
        user_id: int,
        time: datetime,
        is_from_bot: bool,
        text: str,
        db: DB,
        chat: Chat) -> bool:
    if chat.moderation_level == ChatModerationLevelEnum.off.value:
        return False

    is_bad = is_bad_text(text)

    if is_bad:
        await create_bad_message_log(
            db=db,
            chat_id=chat_id,
            chat_name=chat_name,
            user_name=user_name,
            user_id=user_id,
            time=time,
            text=text,
        )
        return True

    if is_from_bot:
        await create_bad_message_log(
            db=db,
            chat_id=chat_id,
            chat_name=chat_name,
            user_name=user_name,
            user_id=user_id,
            time=time,
            text='[SERVICE] Создано с помощью бота',
        )
        return True

    return False
