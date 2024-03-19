from aiogram import F, Router
from aiogram.types import Message

from src.keyboards.chats import (
    get_show_chats_keyboard,
)
from src.repo import DB

router: Router = Router()


@router.message((F.text == 'Добавленные чаты') & (F.chat.type == 'private'))
async def show_chats_list(message: Message, db: DB) -> None:
    await message.answer(
        'Выберите нужную группу',
        reply_markup=await get_show_chats_keyboard(message.from_user.id, db),
    )
