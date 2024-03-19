import asyncio
import concurrent.futures
import os
import time
from typing import Sequence

import aiofiles

from src.models import Log
from src.repo import DB


def process_logs(logs: Sequence[Log]) -> str:
    logs_text = ''
    for log in logs:
        logs_text += f'{log.chat_name} | {log.user_name} | {log.user_id} | {log.message} | {log.time}\n'
    return logs_text


async def create_log_file(chat_id: int,
                          user_id: int,
                          db: DB) -> tuple[bool, str]:
    logs = await db.log.get_list(user_id, chat_id)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        logs_text = await asyncio.get_event_loop().run_in_executor(
            executor,
            process_logs,
            logs,
        )

    if logs_text == '':
        return False, ''

    filename = f'file_for_log{time.time()}.txt'

    async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
        await f.write(logs_text)

    return True, filename


def delete_file(filename: str) -> None:
    try:
        os.remove(filename)
    except:
        pass
