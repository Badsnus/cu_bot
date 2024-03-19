from aiogram import F, Router
from aiogram.types import Message

from src.keyboards import main_menu
from src.repo import DB
from src.services import get_or_create_user

router: Router = Router()


@router.message((F.text == '/start') & (F.chat.type == 'private'))
async def start_handler(message: Message, db: DB) -> None:
    await get_or_create_user(
        user_id=message.from_user.id,
        db=db,
    )

    await message.answer(
        text='Бот админ',
        reply_markup=main_menu,
    )
