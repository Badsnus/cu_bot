from src.repo import DB
from src.services.get_db import get_db


@get_db
async def edit_white_list(chat_id: int,
                          is_add: bool,
                          text: str,
                          db: DB) -> None:
    usernames = set(x.replace('@', '') for x in text.splitlines())

    if not is_add:
        await db.white_list.remove_usernames(chat_id, list(usernames))
        return

    already_have = set(x.username for x in await db.white_list.get_by_chat(chat_id))
    usernames = usernames - already_have

    await db.white_list.add_usernames(chat_id, list(usernames))
