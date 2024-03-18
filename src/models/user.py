from sqlalchemy import (
    BigInteger, Column, Integer,
)

from src.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(BigInteger(), unique=True, index=True)
