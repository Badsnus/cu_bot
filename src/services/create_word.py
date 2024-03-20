from src.repo import DB
from .get_db import get_db


@get_db
async def create_word(word: str, db: DB) -> None:
    await db.word.create(word)
