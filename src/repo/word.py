from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Word
from src.services import MessageChecker


class WordRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, text: str, commit=True) -> Word:
        MessageChecker.bad_words.add(text.lower())
        word = Word(word=text.lower())

        self.session.add(word)
        if commit:
            await self.session.commit()

        return word

    async def get(self, text: str) -> Word | None:
        return await self.session.scalar(
            select(Word).where(Word.word == text),
        )

    async def get_list(self) -> Sequence[Word]:
        return (await self.session.scalars(select(Word))).all()

    async def delete(self, text: str) -> None:
        MessageChecker.bad_words.discard(text.lower())

        await self.session.execute(
            delete(Word).where(Word.word == text),
        )

        await self.session.commit()
