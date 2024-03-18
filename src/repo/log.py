from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Log


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
