from sqlalchemy import (
    Column, Integer, String
)

from src.models import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(
        Integer(),
        primary_key=True,
    )

    word = Column(
        String(length=250),
    )
