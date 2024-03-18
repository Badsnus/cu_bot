from aiogram import Bot
from aiogram.types import ChatMemberAdministrator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Chat, UserChat


class ChatRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     telegram_id: int,
                     chat_name: str,
                     moderation_level=100,
                     commit=True) -> Chat:
        chat = Chat(
            telegram_id=telegram_id,
            chat_name=chat_name,
            moderation_level=moderation_level,
        )

        self.session.add(chat)
        if commit:
            await self.session.commit()

        return chat

    async def get_by_tg_id(self, telegram_id: int) -> Chat | None:
        return await self.session.scalar(
            select(Chat).where(Chat.telegram_id == telegram_id)
        )

    async def update_name(self, chat: Chat, new_chat_name: str) -> Chat:
        chat.chat_name = new_chat_name

        self.session.add(chat)
        await self.session.commit()

        return chat

    async def get_chat_user(self, chat_id: int, user_id: int) -> UserChat | None:
        return await self.session.scalar(
            select(UserChat).where((UserChat.chat_id == chat_id) & (UserChat.user_id == user_id))
        )

    async def add_admins(self,
                         admins: list[ChatMemberAdministrator],
                         chat_id: int,
                         bot: Bot) -> None:
        need_to_add = []
        for admin in admins:
            if admin.user.id != bot.id:
                user_chat = await self.get_chat_user(chat_id, admin.user.id)
                if user_chat is None:
                    need_to_add.append(UserChat(chat_id=chat_id, user_id=admin.user.id))

        self.session.add_all(need_to_add)
        await self.session.commit()
