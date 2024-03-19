from sqlalchemy import (
    BigInteger, Column,
)

from src.models import Base


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(BigInteger(), unique=True, index=True, primary_key=True, autoincrement=False)
