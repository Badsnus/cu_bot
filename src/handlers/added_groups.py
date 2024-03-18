from aiogram import F, Router
from aiogram.types import Message

from src.keyboards import get_show_groups_keyboard
from src.repo import DB

router: Router = Router()


@router.message((F.text == 'Добавленные группы') & (F.chat.type == 'private'))
async def start_handler(message: Message, db: DB) -> None:
    await message.answer(
        'Выберите нужную группу',
        reply_markup=await get_show_groups_keyboard(message.from_user.id, db),
    )
