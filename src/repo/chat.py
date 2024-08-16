from typing import Sequence

from aiogram.types import ChatMemberAdministrator
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Chat, ChatModerationLevelEnum, UserChat
from src.services.generate_invite_code import generate_invite_code


class ChatRepo:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     telegram_id: int,
                     chat_name: str,
                     moderation_level: str = ChatModerationLevelEnum.on.value,
                     channel_telegram_id: int | None = None,
                     commit=True) -> Chat:
        assert moderation_level in ChatModerationLevelEnum.__members__

        while await self.get_by_invite_code(
                invite_code := generate_invite_code()):
            pass

        chat = Chat(
            telegram_id=telegram_id,
            chat_name=chat_name,
            moderation_level=moderation_level,
            invite_code=invite_code,
            channel_telegram_id=channel_telegram_id,
        )

        self.session.add(chat)
        if commit:
            await self.session.commit()

        return chat

    async def get(self, telegram_id: int) -> Chat | None:
        return await self.session.scalar(
            select(Chat).where(Chat.telegram_id == telegram_id)
        )

    async def get_by_channel_id(self, channel_telegram_id: int) -> Chat | None:
        return await self.session.scalar(
            select(Chat).where(Chat.channel_telegram_id == channel_telegram_id)
        )

    async def get_by_invite_code(self, invite_code: str) -> Chat:
        return await self.session.scalar(
            select(Chat).where(Chat.invite_code == invite_code)
        )

    async def update_name_and_telegram_channel_id(
            self,
            chat: Chat,
            new_chat_name: str,
            channel_telegram_id: int) -> Chat:
        f1 = chat.chat_name != new_chat_name
        f2 = chat.channel_telegram_id != channel_telegram_id

        if f1:
            chat.chat_name = new_chat_name
        if f2:
            chat.channel_telegram_id = channel_telegram_id

        if f1 or f2:
            self.session.add(chat)
            await self.session.commit()

        return chat

    async def update_moder_level(self, chat_id: int) -> Chat:
        # пока что так, так как всего два режима
        chat = await self.get(chat_id)

        if chat.moderation_level == ChatModerationLevelEnum.on.value:
            chat.moderation_level = ChatModerationLevelEnum.off.value
        else:
            chat.moderation_level = ChatModerationLevelEnum.on.value

        self.session.add(chat)
        await self.session.commit()

        return chat

    async def update_white_list_status(self, chat_id: int) -> Chat:
        chat = await self.get(chat_id)

        chat.is_white_list_on = not chat.is_white_list_on

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
                need_to_add.append(
                    UserChat(
                        chat_id=chat_id,
                        user_id=admin.user.id,
                    ),
                )

        self.session.add_all(need_to_add)
        await self.session.commit()

    async def add_admin(self,
                        admin_id: int,
                        chat_id: int) -> None:

        self.session.add(UserChat(chat_id=chat_id, user_id=admin_id))
        await self.session.commit()

    async def delete_admin(self, admin_id: int, chat_id: int) -> None:
        await self.session.execute(
            delete(UserChat).where((UserChat.chat_id == chat_id) &
                                   (UserChat.user_id == admin_id))
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
