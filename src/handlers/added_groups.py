from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from src.keyboards.added_groups import (
    ChangeModerLevelCallback,
    GetLogsCallback,
    get_show_groups_keyboard,
    get_retrieve_keyboard,
    RetrieveGroupCallback,
)
from src.models import Chat
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


async def send_chat_retrieve_message(call: CallbackQuery, chat: Chat) -> None:
    await call.message.edit_text(f'Чат {chat.chat_name}\n'
                                 f'Статус модерирования {chat.moderation_level == 100}',
                                 reply_markup=await get_retrieve_keyboard(chat))


@router.callback_query(RetrieveGroupCallback.filter())
async def show_retrieve_group(call: CallbackQuery, callback_data: RetrieveGroupCallback, db: DB) -> None:
    chat = await db.chat.get(callback_data.id)
    await send_chat_retrieve_message(call, chat)


@router.callback_query(ChangeModerLevelCallback.filter())
async def change_level(call: CallbackQuery, callback_data: ChangeModerLevelCallback, db: DB) -> None:
    chat = await db.chat.update_moder_level(callback_data.id)
    await send_chat_retrieve_message(call, chat)
