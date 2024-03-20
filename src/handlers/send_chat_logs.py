from aiogram import Router
from aiogram.types import CallbackQuery, FSInputFile

from src.keyboards.chats_list import GetLogsCallback

from src.services import LogsFile

router: Router = Router()


@router.callback_query(GetLogsCallback.filter())
async def get_logs(call: CallbackQuery,
                   callback_data: GetLogsCallback) -> None:
    await call.message.edit_text('Готовлю логи')

    logs_file = LogsFile(
        chat_id=callback_data.id,
        user_id=call.from_user.id,
    )

    is_create = await logs_file.create()

    if not is_create:
        await call.message.edit_text('Логов нет(')
        return

    await call.message.answer_document(
        document=FSInputFile(logs_file.filename, 'logs.txt'),
        caption='вот твои логи',
    )
    logs_file.delete()
