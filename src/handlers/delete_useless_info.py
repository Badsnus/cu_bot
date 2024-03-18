from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from src.repo import DB
from src.services import update_chat_info

router: Router = Router()


async def create_chat_member_log(message: Message, db: DB, join: bool, bot: Bot) -> None:
    try:
        await message.delete()
        await update_chat_info(message, db, bot)

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
async def on_user_leave(message: Message, db: DB, bot: Bot) -> None:
    await create_chat_member_log(message, db, False, bot)


@router.message(F.new_chat_member)
async def gg(message: Message, db: DB, bot: Bot) -> None:
    await create_chat_member_log(message, db, True, bot)
