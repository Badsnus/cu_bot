from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chat_retrieve import ChangeModerLevelCallback
from src.services import ChatSettingsView

router: Router = Router()


@router.callback_query(ChangeModerLevelCallback.filter())
async def change_level(call: CallbackQuery,
                       callback_data: ChangeModerLevelCallback) -> None:
    settings = ChatSettingsView(callback_data.id)
    text, markup = await settings.update()

    await call.message.edit_text(text, reply_markup=markup)
