from dataclasses import dataclass

from dotenv import load_dotenv

from config.base import getenv


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class Config:
    tg_bot: TelegramBotConfig
    db_connection: str
    log_files_path: str


def load_config() -> Config:
    load_dotenv()

    return Config(
        tg_bot=TelegramBotConfig(token=getenv('BOT_TOKEN')),
        db_connection=getenv('DB_CONNECTION'),
        log_files_path=getenv('LOG_FILES_PATH')
    )
