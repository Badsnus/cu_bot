from aiogram import Bot, F, Router, types

from src.repo import DB
from src.services import create_log_if_message_is_bad, update_chat_info

router: Router = Router()


@router.message(F.chat.type != 'private')
async def chats_messages(message: types.Message, db: DB, bot: Bot) -> None:
    chat = await update_chat_info(message, db, bot, await bot.get_chat_administrators(message.chat.id))

    is_deleted = await create_log_if_message_is_bad(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        user_name=message.from_user.username,
        user_id=message.from_user.id,
        time=message.date,
        is_from_bot=bool(message.via_bot),
        text=message.text,
        db=db,
        chat=chat,
    )

    if is_deleted:
        try:
            await message.delete()
        except:
            pass
