from aiogram import F, Router
from aiogram.types import Message

from src.repo import DB

router: Router = Router()


async def create_chat_member_log(message: Message, db: DB, join: bool) -> None:
    # TODO тут надо обработку ошибок с отправкой куда-то
    await message.delete()
    await db.log.create(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        message='user join' if join else 'user leave',
        time=message.date,
        chat_name=message.chat.title,
        user_name=str(message.from_user.username),
    )


@router.message(F.left_chat_member)
async def on_user_leave(message: Message, db: DB) -> None:
    await create_chat_member_log(message, db, False)


@router.message(F.new_chat_member)
async def gg(message: Message, db: DB) -> None:
    await create_chat_member_log(message, db, True)
