from sqlalchemy import (
    Column, Integer, String
)

from src.models import Base


class Word(Base):
    __tablename__ = 'words'

    word = Column(
        String(length=250),
        primary_key=True,
        autoincrement=False,
    )
