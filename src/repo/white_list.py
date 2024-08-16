from typing import Sequence

from sqlalchemy import and_, delete, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WhiteList


class WhiteListRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_chat(self, chat_id: int) -> Sequence[WhiteList]:
        return (
            await self.session.scalars(select(WhiteList).where(WhiteList.chat_id == chat_id))
        ).all()

    async def remove_usernames(self, chat_id: int, usernames: list[str]) -> None:
        await self.session.execute(
            delete(WhiteList).where(and_(
                WhiteList.chat_id == chat_id,
                WhiteList.username.in_(usernames)
            ))
        )
        await self.session.commit()

    async def add_usernames(self, chat_id: int, usernames: list[str]) -> None:
        units = []
        for username in usernames:
            units.append(WhiteList(
                chat_id=chat_id,
                username=username,
            ))

        self.session.add_all(units)
        await self.session.commit()

    async def check_is_user_in_white_list(self, chat_id: int, username: str) -> bool:
        return await self.session.scalar(
            select(exists().where(and_(WhiteList.chat_id == chat_id, WhiteList.username == username)))
        )

    async def get_user_in_white_list(self, chat_id: int, username: str) -> WhiteList:
        return await self.session.scalar(
            select(WhiteList).filter(and_(WhiteList.chat_id == chat_id, WhiteList.username == username)),
        )

    async def update(self, white_list: WhiteList, telegram_id: int) -> WhiteList:
        white_list.telegram_id = telegram_id

        self.session.add(white_list)
        await self.session.commit()

        return white_list
