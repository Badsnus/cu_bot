from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from src.repo import DB
from src.services import update_chat_info

router: Router = Router()


async def create_chat_member_log(message: Message, db: DB, join: bool, bot: Bot) -> None:
    if join:
        # aiogram lmao??? TODO написать исью
        user_id = message.new_chat_member.get('id')
        user_name = str(message.new_chat_member.get('username'))

        if user_id == message.from_user.id:
            text = 'user join'
        else:
            text = f'user added by {message.from_user.username}'
    else:
        user_id = message.left_chat_member.id
        user_name = str(message.left_chat_member.username)

        if user_id == message.from_user.id:
            text = 'user leave'
        else:
            text = f'user kicked by {message.from_user.username}'

    try:
        await message.delete()
        await update_chat_info(message, db, bot)

        await db.log.create(
            chat_id=message.chat.id,
            user_id=user_id,
            message=text,
            time=message.date,
            chat_name=message.chat.title,
            user_name=user_name,
        )
    except TelegramBadRequest as ex:
        # todo добавить удаление канала, если юзер там не админ мб? типа если он есть в бд - удалить из бд его
        ...


@router.message(F.left_chat_member)
async def on_user_leave(message: Message, db: DB, bot: Bot) -> None:
    if message.left_chat_member.id != bot.id:
        await create_chat_member_log(message, db, False, bot)
        return
    await db.chat.delete(message.chat.id)


@router.message(F.new_chat_member)
async def gg(message: Message, db: DB, bot: Bot) -> None:
    await create_chat_member_log(message, db, True, bot)
