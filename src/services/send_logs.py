import asyncio
import concurrent.futures
import os
import time
from typing import Sequence

from aiogram.types import CallbackQuery, FSInputFile

from src.models import Log
from src.repo import DB


def process_logs(logs: Sequence[Log]) -> str:
    logs_text = ''
    for log in logs:
        logs_text += f'{log.chat_name} | {log.user_name} | {log.message} | {log.time}\n'
    return logs_text


async def send_logs(call: CallbackQuery, db: DB, id: int) -> None:
    try:
        await call.message.edit_text('Готовлю логи')
    except:
        pass

    logs = await db.log.get_logs(call.from_user.id, id)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        logs_text = await asyncio.get_event_loop().run_in_executor(
            executor,
            process_logs,
            logs,
        )

    if logs_text == '':
        await call.answer('Логов нет')
        return

    filename = f'file_for_log{time.time()}.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(logs_text)
    await call.message.answer_document(document=FSInputFile(filename), caption='logs')

    try:
        os.remove(filename)
    except:
        pass
