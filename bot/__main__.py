import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from bot import routers
from bot.middleware.db_session_middleware import DatabaseSessionMiddleware
from bot.middleware.register_check import RegisterCheck
from bot.services.db.engine import create_db_session
from bot.services.logging.logger import logger
from bot.settings import Settings


async def main() -> None:
    cfg = Settings()
    bot = Bot(token=cfg.BOT_TOKEN, parse_mode='HTML')

    dispatcher = Dispatcher(bot=bot, storage=MemoryStorage() if not cfg.REDIS_DSN else RedisStorage.from_url(
        url=cfg.REDIS_DSN
    ))

    session_maker = await create_db_session(cfg)

    dispatcher.update.middleware(DatabaseSessionMiddleware(
        session_maker=session_maker,
    ))

    dispatcher.message.middleware(RegisterCheck())
    dispatcher.callback_query.middleware(RegisterCheck())

    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())
    routers.setup(dp=dispatcher)

    await dispatcher.start_polling(
        bot,
        logger=logger,
        allowed_updates=dispatcher.resolve_used_update_types()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
