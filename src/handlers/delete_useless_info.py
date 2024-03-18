from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from src.repo import DB

router: Router = Router()


async def create_chat_member_log(message: Message, db: DB, join: bool) -> None:
    try:
        await message.delete()
        chat = await db.chat.get_by_tg_id(message.chat.id)
        if chat is None:
            chat = await db.chat.create(telegram_id=message.chat.id, chat_name=message.chat.title)

        if chat.chat_name != message.chat.title:
            chat = await db.chat.update_name(chat, message.chat.title)

        await db.log.create(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message='user join' if join else 'user leave',
            time=message.date,
            chat_name=message.chat.title,
            user_name=str(message.from_user.username),
        )
    except TelegramBadRequest as ex:
        # todo добавить удаление канала, если юзер там не админ мб? типа если он есть в бд - удалить из бд его
        ...


@router.message(F.left_chat_member)
async def on_user_leave(message: Message, db: DB) -> None:
    await create_chat_member_log(message, db, False)


@router.message(F.new_chat_member)
async def gg(message: Message, db: DB) -> None:
    await create_chat_member_log(message, db, True)
