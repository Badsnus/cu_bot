from aiogram import Bot, F, Router, types

from src.services import (
    check_is_message_from_bot,
    create_bad_message_log,
    MessageChecker,
    update_chat_info,
)

router: Router = Router()


@router.edited_message(F.chat.type != 'private')
@router.message(F.chat.type != 'private')
async def chats_messages(message: types.Message, bot: Bot) -> None:
    chat = await update_chat_info(
        chat_id=message.chat.id,
        chat_name=message.chat.title,
        get_admins_method=bot.get_chat_administrators,
        bot_id=bot.id,
    )

    text = message.text or message.caption or ''

    is_message_from_bot = await check_is_message_from_bot(message.via_bot)
    is_from_channel = message.from_user.is_bot

    is_good = MessageChecker(
        chat=chat,
        text=text,
        is_from_bot=is_message_from_bot,
        is_from_channel=is_from_channel,
    ).check()

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
