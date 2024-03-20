import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import Config, load_config
from src.handlers import routers
from src.middlewares import DbSessionMiddleware
from src.models import Base, db_engine, db_session_maker

logger = logging.getLogger(__name__)

config: Config = load_config()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info('Starting bot')

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot: Bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )
    dp: Dispatcher = Dispatcher()

    dp.include_routers(*routers)
    dp.update.middleware(DbSessionMiddleware(session_pool=db_session_maker))

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
