from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.keyboards import get_show_groups_keyboard
from src.keyboards.added_groups import get_show_groups_keyboard, GetLogsCallback, RetrieveGroupCallback
from src.repo import DB
from src.services import send_logs

router: Router = Router()


@router.message((F.text == 'Добавленные группы') & (F.chat.type == 'private'))
async def start_handler(message: Message, db: DB) -> None:
    await message.answer(
        'Выберите нужную группу',
        reply_markup=await get_show_groups_keyboard(message.from_user.id, db),
    )


@router.callback_query(GetLogsCallback.filter())
async def get_logs(call: CallbackQuery, callback_data: GetLogsCallback, db: DB) -> None:
    await send_logs(call, db, callback_data.id)
