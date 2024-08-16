from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chat_retrieve import (
    AddWhiteListMemberCallback,
    DeleteWhiteListMemberCallback,
    GetWhiteListMembersCallback,
)
from src.services import ChatSettingsView
from src.services.send_white_list_file import send_white_list_file

router: Router = Router()


@router.callback_query(GetWhiteListMembersCallback.filter())
async def change_white_list_status(call: CallbackQuery,
                                   callback_data: GetWhiteListMembersCallback) -> None:
    try:
        await call.message.delete()
    except:  # todo obrabotat
        pass

    await send_white_list_file(callback_data.id, call)

    settings = ChatSettingsView(callback_data.id)
    text, markup = await settings.get()

    await call.message.answer(text, reply_markup=markup)
