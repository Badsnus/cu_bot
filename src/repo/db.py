from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserRepo


class DB:

    def __init__(self, session: AsyncSession):
        self.user: UserRepo = UserRepo(session)