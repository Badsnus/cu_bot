from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


class UserRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, telegram_id: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

    async def create(self,
                     telegram_id: int,
                     is_admin: bool = False,
                     commit=True) -> User:
        user = User(telegram_id=telegram_id, is_admin=is_admin)

        self.session.add(user)
        if commit:
            await self.session.commit()

        return user
