from enum import Enum

from sqlalchemy import (
    BigInteger, Column, Integer, String,
)

from src.models import Base


class ChatModerationLevelEnum(Enum):
    on = 'on'
    off = 'off'


class Chat(Base):
    __tablename__ = 'chats'

    telegram_id = Column(
        BigInteger(),
        unique=True,
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    chat_name = Column(
        String(130),
    )

    moderation_level = Column(
        String(10),
        default=ChatModerationLevelEnum.on,
    )


class UserChat(Base):
    __tablename__ = 'users_chats'

    id = Column(Integer(), primary_key=True)

    user_id = Column(BigInteger())
    chat_id = Column(BigInteger())
