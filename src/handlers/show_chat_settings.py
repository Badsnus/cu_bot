from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chats import (
    get_retrieve_keyboard,
    RetrieveGroupCallback,
)
from src.repo import DB

router: Router = Router()


@router.callback_query(RetrieveGroupCallback.filter())
async def show_chat_settings(call: CallbackQuery, callback_data: RetrieveGroupCallback, db: DB) -> None:
    chat = await db.chat.get_by_tg_id(callback_data.id)

    await call.message.edit_text(
        f'Чат {chat.chat_name}\n'
        f'Статус модерирования {chat.moderation_level}',
        reply_markup=await get_retrieve_keyboard(chat),
    )
