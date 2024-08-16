from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chat_retrieve import ToggleWhiteListCallback
from src.services import ChatSettingsView

router: Router = Router()


@router.callback_query(ToggleWhiteListCallback.filter())
async def change_white_list_status(call: CallbackQuery,
                                   callback_data: ToggleWhiteListCallback) -> None:
    settings = ChatSettingsView(callback_data.id)
    text, markup = await settings.update_white_list_status()

    await call.message.edit_text(text, reply_markup=markup)
