from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.models import Log, UserChat, Chat


class LogRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     chat_id: int,
                     user_id: int,
                     message: str,
                     time: datetime,
                     chat_name: str,
                     user_name: str,
                     commit=True) -> Log:
        log = Log(
            chat_id=chat_id,
            user_id=user_id,
            message=message,
            time=time,
            chat_name=chat_name,
            user_name=user_name,
        )

        self.session.add(log)
        if commit:
            await self.session.commit()

        return log

    async def get_logs(self, user_id: int, chat_id: int) -> Sequence[Log]:
        print(chat_id)
        query = (
            select(Log)
            .join(UserChat, Log.chat_id == UserChat.chat_id)
            .where(UserChat.user_id == user_id)
        )

        if chat_id != -1:
            query = query.where(Log.chat_id == chat_id)

        return (await self.session.scalars(query)).all()
