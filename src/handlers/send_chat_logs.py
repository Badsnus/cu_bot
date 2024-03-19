from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from src.keyboards.chats_list import (
    GetLogsCallback,
)
from src.repo import DB
from src.services import create_log_file
from src.services.prepare_logs import delete_file

router: Router = Router()


@router.callback_query(GetLogsCallback.filter())
async def get_logs(call: CallbackQuery, callback_data: GetLogsCallback, db: DB) -> None:
    await call.message.edit_text('Готовлю логи')

    created, filename = await create_log_file(
        chat_id=callback_data.id,
        user_id=call.from_user.id,
        db=db,
    )

    if not created:
        await call.message.edit_text('Логов нет(')
        return

    await call.message.answer_document(document=FSInputFile(filename), caption='вот твои логи')
    delete_file(filename)
