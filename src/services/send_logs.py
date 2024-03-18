import time

from aiogram.types import CallbackQuery, FSInputFile

from src.repo import DB


async def send_logs(call: CallbackQuery, db: DB, id: int) -> None:
    try:
        await call.message.edit_text('Готовлю логи')
    except:
        pass

    logs = await db.log.get_logs(call.from_user.id, id)

    logs_text = ''
    for log in logs:
        logs_text += f'{log.chat_name} | {log.user_name} | {log.message} | {log.time}\n'

    filename = f'file_for_log{time.time()}.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(logs_text)
    await call.message.answer_document(document=FSInputFile(filename), caption='logs')
