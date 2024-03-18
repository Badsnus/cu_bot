from aiogram import F, Router
from aiogram.types import Message

from src.keyboards import main_menu

router: Router = Router()


@router.message((F.text == '/start') & (F.chat.type == 'private'))
async def start_handler(message: Message) -> None:
    await message.answer(text='Бот админ',
                         reply_markup=main_menu)
