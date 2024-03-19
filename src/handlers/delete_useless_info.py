from aiogram import Bot, F, Router
from aiogram.types import Message

from src.repo import DB
from src.services import update_chat_info
from src.services.check_is_bot_kicked_and_create_log import (
    check_is_bot_kicked_or_member_and_create_log,
)
from src.services.create_service_notig_log import (
    create_member_join_log,
)

router: Router = Router()


async def update_chat_info_and_delete_message(message: Message,
                                              db: DB,
                                              bot: Bot) -> None:
    await update_chat_info(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        admins=await bot.get_chat_administrators(message.chat.id),
        bot_id=bot.id,
        db=db,
    )

    try:
        await message.delete()
    except Exception:
        pass


@router.message(F.left_chat_member)
async def on_user_leave(message: Message, db: DB, bot: Bot) -> None:
    await check_is_bot_kicked_or_member_and_create_log(
        bot_id=bot.id,
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        message_time=message.date,
        member_user_id=message.left_chat_member.id,
        member_user_name=message.left_chat_member.username,
        from_user_id=message.from_user.id,
        from_user_username=message.from_user.username,
        db=db,
    )

    await update_chat_info_and_delete_message(message, db, bot)


@router.message(F.new_chat_member)
async def on_user_join(message: Message, db: DB, bot: Bot) -> None:
    await create_member_join_log(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        message_time=message.date,
        member_user_id=message.new_chat_member.get('id'),
        member_user_name=message.new_chat_member.get('username'),
        from_user_id=message.from_user.id,
        from_user_username=message.from_user.username,
        db=db,
    )

    await update_chat_info_and_delete_message(message, db, bot)
