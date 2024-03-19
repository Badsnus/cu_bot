from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chats import (
    ChangeModerLevelCallback,
    get_retrieve_keyboard,
)
from src.repo import DB

router: Router = Router()


@router.callback_query(ChangeModerLevelCallback.filter())
async def change_level(call: CallbackQuery, callback_data: ChangeModerLevelCallback, db: DB) -> None:
    chat = await db.chat.update_moder_level(callback_data.id)

    await call.message.edit_text(
        f'Чат {chat.chat_name}\n'
        f'Статус модерирования {chat.moderation_level}',
        reply_markup=await get_retrieve_keyboard(chat),
    )
