from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import WhiteList


class WhiteListRepo:

    def __init__(self, session: AsyncSession):
        self.session = session
