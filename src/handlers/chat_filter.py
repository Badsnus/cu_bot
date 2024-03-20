from aiogram import Bot, F, Router, types

from src.repo import DB
from src.services import (
    create_bad_message_log,
    check_is_message_good,
    check_is_message_from_bot,
    update_chat_info,
)

router: Router = Router()


@router.message(F.chat.type != 'private')
async def chats_messages(message: types.Message, db: DB, bot: Bot) -> None:
    chat = await update_chat_info(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        admins=await bot.get_chat_administrators(message.chat.id),
        bot_id=bot.id,
        db=db,
    )

    text = message.text or message.caption or ''

    is_message_from_bot = await check_is_message_from_bot(message.via_bot)

    is_good = await check_is_message_good(
        chat=chat,
        text=text,
        is_from_bot=is_message_from_bot,
    )

    if is_good:
        return

    await create_bad_message_log(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        user_name=message.from_user.username,
        user_id=message.from_user.id,
        time=message.date,
        text=text,
        is_from_bot=is_message_from_bot,
    )

    try:
        await message.delete()
    except Exception:
        pass
