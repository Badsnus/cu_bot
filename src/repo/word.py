from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Word
from src.services import IsMessageGood


class WordRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self) -> Sequence[Word]:
        return (await self.session.scalars(select(Word))).all()

    async def create(self, text: str, commit=True) -> Word:
        IsMessageGood.bad_words.add(text)
        word = Word(word=text.lower())

        self.session.add(word)
        if commit:
            await self.session.commit()

        return word
