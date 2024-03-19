from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig
    db_connection: str


def load_config() -> Config:
    load_dotenv()

    return Config(
        tg_bot=TelegramBotConfig(token=getenv('BOT_TOKEN')),
        db_connection=getenv('db_connection'),
    )


def load_test_database_url() -> str:
    load_dotenv()
    return getenv('test_db_connection')
