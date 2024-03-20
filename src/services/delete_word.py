from src.repo import DB
from .get_db import get_db


@get_db
async def delete_word(text: str, db: DB) -> bool:
    text = text.lower()

    word = await db.word.get(text)

    if word is None:
        return False

    await db.word.delete(word.word)

    return True
