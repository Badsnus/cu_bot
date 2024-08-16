from sqlalchemy import (
    BigInteger, Column, Integer
)

from src.models import Base


class WhiteList(Base):
    __tablename__ = 'white_list'

    id = Column(Integer, primary_key=True)

    telegram_id = Column(
        BigInteger(),
    )
    chat_id = Column(
        BigInteger(),
    )
