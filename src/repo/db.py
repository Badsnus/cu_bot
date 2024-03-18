from sqlalchemy.ext.asyncio import AsyncSession

from .chat import ChatRepo
from .log import LogRepo
from .user import UserRepo


class DB:

    def __init__(self, session: AsyncSession):
        self.user: UserRepo = UserRepo(session)
        self.log: LogRepo = LogRepo(session)
        self.chat: ChatRepo = ChatRepo(session)
