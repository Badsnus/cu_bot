from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards.chats_list import (
    get_show_chats_keyboard,
)

router: Router = Router()


@router.message((F.text == 'Добавленные чаты') & (F.chat.type == 'private'))
async def show_chats_list(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        'Выберите нужную группу',
        reply_markup=await get_show_chats_keyboard(message.from_user.id),
    )
