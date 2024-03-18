from aiogram import F, Router
from aiogram.types import Message

from src.keyboards import main_menu
from src.repo import DB

router: Router = Router()


@router.message((F.text == '/start') & (F.chat.type == 'private'))
async def start_handler(message: Message, db: DB) -> None:
    await db.user.get_or_create(message.from_user.id)

    await message.answer(text='Бот админ',
                         reply_markup=main_menu)
