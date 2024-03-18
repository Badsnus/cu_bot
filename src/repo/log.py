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

    async def get_logs(self, user_id: int) -> Sequence[Log]:
        user_chat_alias = aliased(UserChat)
        query = (
            select(Log)
            .join_from(UserChat, Log, Log.chat_id == user_chat_alias.chat_id)
            .where(user_chat_alias.user_id == user_id)
        )

        return (await self.session.scalars(query)).all()
