from aiogram import Bot, F, Router
from aiogram.types import Message

from src.services import delete_chat, ServiceMessageLogger, update_chat_info

router: Router = Router()


async def update_chat_info_and_delete_message(message: Message,
                                              bot: Bot) -> None:
    await update_chat_info(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        get_admins_method=bot.get_chat_administrators,
        bot_id=bot.id
    )

    try:
        await message.delete()
    except Exception:
        pass


@router.message(F.left_chat_member)
async def on_user_leave(message: Message, bot: Bot) -> None:
    if bot.id == message.left_chat_member.id:
        await delete_chat(chat_id=message.chat.id)
        return

    logger = ServiceMessageLogger(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        message_time=message.date,
        member_user_id=message.left_chat_member.id,
        member_user_name=message.left_chat_member.username,
        from_user_id=message.from_user.id,
        from_user_username=message.from_user.username,
    )
    await logger.create_leave_log()

    await update_chat_info_and_delete_message(message, bot)


@router.message(F.new_chat_member)
async def on_user_join(message: Message, bot: Bot) -> None:
    logger = ServiceMessageLogger(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        message_time=message.date,
        member_user_id=message.new_chat_member.get('id'),
        member_user_name=message.new_chat_member.get('username'),
        from_user_id=message.from_user.id,
        from_user_username=message.from_user.username,
    )
    await logger.create_join_log()

    await update_chat_info_and_delete_message(message, bot)
