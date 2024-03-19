import re

from aiogram.types import Message

from src.models import Chat
from src.repo import DB

# todo офк надо отсюда вынести
bad_words = set(open('bad_words.txt', encoding='utf-8').read().splitlines())


def is_bad_text(text: str) -> bool:
    words = set(re.findall(r'\w+', text))
    return bool(words & bad_words)


def is_from_bot(message: Message) -> bool:
    return bool(message.via_bot)


async def delete_message_and_create_log(db: DB, message: Message, text: str) -> None:
    try:
        await message.delete()

        await db.log.create(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message=text,
            time=message.date,
            chat_name=message.chat.title,
            user_name=message.from_user.username,
        )
    except:
        # todo ошибку надо обработать
        pass


async def delete_bad_message(message: Message, db: DB, chat: Chat) -> None:
    text = message.text or message.caption or ''

    is_bad = is_bad_text(text)

    if is_bad and chat.moderation_level != 0:
        await delete_message_and_create_log(db, message, text)

    if is_from_bot(message):
        await delete_message_and_create_log(db, message, 'создано ботом')
