from sqlalchemy import (
    BigInteger, Column, Integer,
)

from src.models import Base


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), unique=True, index=True)

    moderation_level = Column(Integer(), default=100)
