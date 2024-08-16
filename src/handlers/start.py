from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards import get_main_menu
from src.services import get_or_create_user
from src.services.check_access_to_channel import check_access_to_chat

router: Router = Router()


@router.message((F.text == '/start') & (F.chat.type == 'private'))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    user = await get_or_create_user(
        user_id=message.from_user.id,
    )

    await message.answer(
        text='Цу модератор',
        reply_markup=get_main_menu(user.is_admin),
    )


@router.message((F.text.startswith('/start')) & (F.chat.type == 'private'))
async def check_invite_link(message: Message, bot: Bot) -> None:
    try:
        invite_code = message.text.split(' ')[1]
    except IndexError:
        await message.answer('?')
        return

    text = await check_access_to_chat(
        invite_code,
        message.from_user.username,
        bot,
    )
    await message.answer(text, disable_web_page_preview=True)
