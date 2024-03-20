from datetime import datetime

from src.repo import DB
from src.services.get_db import get_db


class ServiceMessageLogger:

    def __init__(self,
                 chat_id: int,
                 chat_name: str,
                 message_time: datetime,
                 member_user_id: int,
                 member_user_name: str,
                 from_user_id: int,
                 from_user_username: str) -> None:
        self._chat_id = chat_id
        self._chat_name = chat_name
        self._message_time = message_time
        self._member_user_id = member_user_id
        self._member_user_name = member_user_name
        self._from_user_id = from_user_id
        self._from_user_username = from_user_username

    @property
    def _leave_text(self) -> str:
        return ('user leave'
                if self._member_user_id == self._from_user_id
                else f'user kicked by {self._from_user_username}')

    @property
    def _join_text(self) -> str:
        return ('user join'
                if self._member_user_id == self._from_user_id
                else f'user added by {self._from_user_username}')

    @get_db
    async def __create_log(self, text: str, db: DB) -> None:
        await db.log.create(
            chat_id=self._chat_id,
            user_id=self._member_user_id,
            message='[ServiceMessage] ' + text,
            time=self._message_time,
            chat_name=self._chat_name,
            user_name=self._member_user_name,
        )

    async def create_leave_log(self) -> None:
        await self.__create_log(self._leave_text)

    async def create_join_log(self) -> None:
        await self.__create_log(self._join_text)
