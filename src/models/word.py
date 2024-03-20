from sqlalchemy import (
    Column, String
)

from src.models import Base


class Word(Base):
    __tablename__ = 'words'

    word = Column(
        String(length=250),
        primary_key=True,
        autoincrement=False,
    )
