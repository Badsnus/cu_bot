from sqlalchemy import (
    BigInteger, Column, Integer, String
)

from src.models import Base


class WhiteList(Base):
    __tablename__ = 'white_list'

    id = Column(Integer, primary_key=True)

    username = Column(
        String(300),
    )
    telegram_id = Column(
        BigInteger(),
        nullable=True,
    )
    chat_id = Column(
        BigInteger(),
    )
