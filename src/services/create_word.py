from .get_db import get_db


async def create_word(word: str) -> None:
    db = await get_db()
    await db.word.create(word)
