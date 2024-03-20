from sqlalchemy import (
    BigInteger, Boolean, Column,
)

from src.models import Base


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(
        BigInteger(),
        unique=True,
        index=True,
        primary_key=True,
        autoincrement=False,
    )

    is_admin = Column(
        Boolean(),
        default=False,
    )
