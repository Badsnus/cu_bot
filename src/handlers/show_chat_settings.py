from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chats import RetrieveGroupCallback
from src.repo import DB
from src.services import get_chat_settings_text_and_keyboard

router: Router = Router()


@router.callback_query(RetrieveGroupCallback.filter())
async def show_chat_settings(call: CallbackQuery, callback_data: RetrieveGroupCallback, db: DB) -> None:
    text, markup = get_chat_settings_text_and_keyboard(chat_id=callback_data.id, db=db)

    await call.message.edit_text(text, reply_markup=markup)
