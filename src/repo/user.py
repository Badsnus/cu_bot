from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class UserRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_tg_id(self, telegram_id: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

    async def get(self, id: int) -> User | None:
        return await self.session.scalar(select(User).where(User.id == id))
