from typing import Sequence

from aiogram.types import ChatMemberAdministrator
from sqlalchemy import delete, select
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

    async def get(self, telegram_id: int) -> Chat | None:
        return await self.session.scalar(
            select(Chat).where(Chat.telegram_id == telegram_id)
        )

    async def update_name(self, chat: Chat, new_chat_name: str) -> Chat:
        chat.chat_name = new_chat_name

        self.session.add(chat)
        await self.session.commit()

        return chat

    async def update_moder_level(self, chat_id: int) -> Chat:
        # костыль так как пока что включенная модерация - это больше нуля
        # а по дефолту стоит 100 - это типа минимальная планка отсева должна быть
        chat = await self.get(chat_id)
        chat.moderation_level = 100 - chat.moderation_level

        self.session.add(chat)
        await self.session.commit()

        return chat

    async def add_admins(self,
                         admins: list[ChatMemberAdministrator],
                         chat_id: int,
                         bot_id: int) -> None:

        need_to_add = []
        for admin in admins:
            if admin.user.id != bot_id:
                need_to_add.append(UserChat(chat_id=chat_id, user_id=admin.user.id))

        self.session.add_all(need_to_add)
        await self.session.commit()

    async def add_admin(self,
                        admin_id: int,
                        chat_id: int) -> None:

        self.session.add(UserChat(chat_id=chat_id, user_id=admin_id))
        await self.session.commit()

    async def delete_admin(self, admin_id: int, chat_id: int) -> None:
        await self.session.execute(
            delete(UserChat).where((UserChat.chat_id == chat_id) & (UserChat.user_id == admin_id))
        )
        await self.session.commit()

    async def get_chats_by_user(self, user_id: int) -> Sequence[Chat]:
        query = (
            select(Chat)
            .join(UserChat, Chat.telegram_id == UserChat.chat_id)
            .where(UserChat.user_id == user_id)
        )

        return (await self.session.scalars(query)).all()

    async def delete(self, chat_id: int) -> None:
        await self.session.execute(
            delete(UserChat).where(UserChat.chat_id == chat_id)
        )
        await self.session.execute(
            delete(Chat).where(Chat.telegram_id == chat_id)
        )
        await self.session.commit()
