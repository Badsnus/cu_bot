from sqlalchemy import (
    BigInteger, Column, Integer, DateTime, String,
)

from src.models import Base


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer(), primary_key=True)

    chat_id = Column(BigInteger())
    user_id = Column(BigInteger())
    message = Column(String(4100))
    time = Column(DateTime())
    chat_name = Column(String(130))
    user_name = Column(String(40))
