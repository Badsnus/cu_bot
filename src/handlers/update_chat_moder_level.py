from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chat_retrieve import ChangeModerLevelCallback
from src.repo import DB
from src.services import update_chat_settings_and_get_text_and_keyboard

router: Router = Router()


@router.callback_query(ChangeModerLevelCallback.filter())
async def change_level(call: CallbackQuery, callback_data: ChangeModerLevelCallback, db: DB) -> None:
    text, markup = await update_chat_settings_and_get_text_and_keyboard(chat_id=callback_data.id, db=db)

    await call.message.edit_text(text, reply_markup=markup)
