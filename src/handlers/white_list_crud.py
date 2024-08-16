import os
import uuid

from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.chat_retrieve import (
    ChangeWhiteListMemberCallback,
    GetWhiteListMembersCallback,
)
from src.keyboards.chats_list import get_back_keyboard
from src.services import ChatSettingsView
from src.services.edit_white_list import edit_white_list
from src.services.send_white_list_file import send_white_list_file
from src.states.edit_white_list import EditWhiteList

router: Router = Router()


@router.callback_query(GetWhiteListMembersCallback.filter())
async def change_white_list_status(call: CallbackQuery,
                                   callback_data: GetWhiteListMembersCallback,
                                   ) -> None:
    try:
        await call.message.delete()
    except Exception:  # todo obrabotat
        pass

    await send_white_list_file(callback_data.id, call)

    settings = ChatSettingsView(callback_data.id)
    text, markup = await settings.get()

    await call.message.answer(text, reply_markup=markup)


@router.callback_query(ChangeWhiteListMemberCallback.filter())
async def ask_file(call: CallbackQuery,
                   callback_data: ChangeWhiteListMemberCallback,
                   state: FSMContext) -> None:
    await state.update_data(
        is_add=callback_data.is_add,
        chat_id=callback_data.id,
    )
    text = '<b>' + ('ДОБАВИТЬ в'
                    if callback_data.is_add
                    else 'УДАЛИТЬ из') + '</b>'

    await call.message.edit_text(
        f'Пришлите txt файл - список пользователей,'
        f' который вы хотите {text} в white list\n\n'
        f'<b>Формат:</b>\n<code>@username1\nusername2\n'
        f'username3\n@username4</code>',
        reply_markup=get_back_keyboard(callback_data.id),
    )

    await state.set_state(EditWhiteList.file)


@router.message(EditWhiteList.file)
async def edit_white_list_handler(message: Message,
                                  state: FSMContext,
                                  bot: Bot) -> None:
    data = await state.get_data()
    chat_id = data.get('chat_id')
    is_add = data.get('is_add')

    if None in (chat_id, is_add):
        await message.answer('Произошла ошибка')
        return
    if message.document is None:
        await message.answer(
            'Пришлите документ',
            reply_markup=get_back_keyboard(chat_id),
        )
        return

    await state.clear()

    filename = str(uuid.uuid4()) + '.txt'
    await bot.download(message.document, destination=filename)

    with open(filename, encoding='utf-8') as file:
        text = file.read()
    try:
        os.remove(filename)
    except Exception:
        pass

    await edit_white_list(chat_id, is_add, text)

    settings = ChatSettingsView(chat_id)
    text, markup = await settings.get()

    await message.answer(text, reply_markup=markup)
