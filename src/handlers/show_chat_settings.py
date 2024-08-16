from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.keyboards.chats_list import RetrieveChatCallback
from src.services import ChatSettingsView

router: Router = Router()


@router.callback_query(RetrieveChatCallback.filter())
async def show_chat_settings(call: CallbackQuery,
                             callback_data: RetrieveChatCallback,
                             state: FSMContext) -> None:
    await state.clear()

    settings = ChatSettingsView(callback_data.id)
    text, markup = await settings.get()

    await call.message.edit_text(text, reply_markup=markup)
