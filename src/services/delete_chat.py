from src.repo import DB
from src.services.get_db import get_db


@get_db
async def delete_chat(chat_id: int, db: DB) -> None:
    await db.chat.delete(chat_id)
