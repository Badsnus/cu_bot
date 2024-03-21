import asyncio
import concurrent.futures
import os
import time
from typing import Sequence

import aiofiles

from config import load_config
from src.models import Log
from src.repo import DB
from src.services.get_db import get_db


class LogFile:
    __path = None

    def _generate_filename(self) -> str:
        return f'{self.__path}file_for_log{self._user_id}_{time.perf_counter()}.txt'

    def __init__(self,
                 chat_id: int,
                 user_id: int) -> None:
        self._user_id = user_id
        self._chat_id = chat_id

        if LogFile.__path is None:
            LogFile.__path = self.__path = load_config().log_files_path

        self._filename = self._generate_filename()

    @property
    def filename(self) -> str:
        return self._filename

    @staticmethod
    def _get_logs_text(logs: Sequence[Log]) -> str:
        return '\n'.join(
            f'{log.chat_name} | {log.user_name} | {log.user_id} | '
            f'{log.message} | {log.time}' for log in logs
        )

    @get_db
    async def create(self, db: DB) -> bool:
        logs = await db.log.get_list(self._user_id, self._chat_id)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            logs_text = await asyncio.get_event_loop().run_in_executor(
                executor,
                self._get_logs_text,
                logs,
            )

        if logs_text == '':
            return False

        async with aiofiles.open(self.filename, 'w', encoding='utf-8') as f:
            await f.write(logs_text)

        return True

    def delete(self):
        try:
            os.remove(self.filename)
        except Exception:
            pass
