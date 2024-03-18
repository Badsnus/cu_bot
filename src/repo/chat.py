from typing import Sequence

from aiogram import Bot
from aiogram.types import ChatMemberAdministrator
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

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

    async def get(self, id: int) -> Chat | None:
        return await self.session.scalar(
            select(Chat).where(Chat.id == id)
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
                need_to_add.append(UserChat(chat_id=chat_id, user_id=admin.user.id))

        self.session.add_all(need_to_add)
        await self.session.commit()

    async def add_admin(self,
                        admin_id: int,
                        chat_id: int,
                        bot: Bot) -> None:

        need_to_add = []
        if admin_id != bot.id:
            need_to_add.append(UserChat(chat_id=chat_id, user_id=admin_id))
        else:
            assert 'ASDASDASDASD' == '1'

        self.session.add_all(need_to_add)
        await self.session.commit()

    async def delete_admin(self, admin_id: int, chat_id: int) -> None:
        await self.session.execute(
            delete(UserChat).where((UserChat.chat_id == chat_id) & (UserChat.user_id == admin_id))
        )
        await self.session.commit()

    async def get_chats_by_user(self, user_id: int) -> Sequence[Chat]:
        user_chat_alias = aliased(UserChat)
        query = (
            select(Chat)
            .join_from(UserChat, Chat, Chat.telegram_id == user_chat_alias.chat_id)
            .where(user_chat_alias.user_id == user_id)
        )

        return (await self.session.scalars(query)).all()
