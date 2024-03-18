import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import Config, load_config
from src.handlers import routers
from src.middlewares import DbSessionMiddleware
from src.models import Base

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info('Starting bot')

    config: Config = load_config()

    engine = create_async_engine(url=config.db_connection, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot: Bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )
    dp: Dispatcher = Dispatcher()

    dp.include_routers(*routers)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')
