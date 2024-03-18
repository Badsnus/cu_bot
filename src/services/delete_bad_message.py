import re

from aiogram.types import Message

from src.repo import DB

# todo офк надо отсюда вынести
bad_words = set(open('bad_words.txt', encoding='utf-8').read().splitlines())


async def is_bad_text(text):
    words = set(re.findall(r'\w+', text))
    return bool(words & bad_words)


async def delete_bad_message(message: Message, db: DB) -> None:
    is_bad = await is_bad_text(message.text)
    if is_bad:
        try:
            await message.delete()

            await db.log.create(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                message=message.text,
                time=message.date,
                chat_name=message.chat.title,
                user_name=message.from_user.username,
            )
        except:
            # todo ошибку надо обработать
            pass
