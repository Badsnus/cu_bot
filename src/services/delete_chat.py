from src.services.get_db import get_db


async def delete_chat(chat_id: int) -> None:
    db = await get_db()
    await db.chat.delete(chat_id)
