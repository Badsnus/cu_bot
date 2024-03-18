from sqlalchemy import (
    BigInteger, Column, Integer, ForeignKey, String, Table,
)

from src.models import Base


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), unique=True, index=True)

    chat_name = Column(String(130))

    moderation_level = Column(Integer(), default=100)


class UserChat(Base):
    __tablename__ = 'users_chats'

    id = Column(Integer(), primary_key=True)

    user_id = Column(BigInteger())
    chat_id = Column(BigInteger())

