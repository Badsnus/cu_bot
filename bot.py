import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import Config, load_config
from src.handlers import routers
from src.models import Base, db_engine
from src.services import clear_old_logs, get_db, MessageChecker, ChatSettingsView

logger = logging.getLogger(__name__)

config: Config = load_config()


@get_db.get_db
async def main(db) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info('Starting bot')

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    MessageChecker.bad_words = {x.word for x in await db.word.get_list()}
    asyncio.create_task(clear_old_logs())

    bot: Bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )
    dp: Dispatcher = Dispatcher()

    ChatSettingsView.bot_link = (await bot.get_me()).username

    dp.include_routers(*routers)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
