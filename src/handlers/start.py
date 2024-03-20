from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards import get_main_menu
from src.services import get_or_create_user

router: Router = Router()


@router.message((F.text == '/start') & (F.chat.type == 'private'))
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    user = await get_or_create_user(
        user_id=message.from_user.id,
    )

    await message.answer(
        text='Бот админ',
        reply_markup=get_main_menu(user.is_admin),
    )
