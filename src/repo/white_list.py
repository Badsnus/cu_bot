from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WhiteList


class WhiteListRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_chat(self, chat_id: int) -> Sequence[WhiteList]:
        return (
            await self.session.scalars(select(WhiteList).where(WhiteList.chat_id == chat_id))
        ).all()
