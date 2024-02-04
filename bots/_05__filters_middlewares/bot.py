import asyncio
import logging

from aiogram import Bot, Dispatcher

from bots.config_reader import get_bot_config
from handlers import group_emojies, checkin, usernames, common
from middlewares.weekend import WeekendCallbackMiddleware


async def main():
    bot = Bot(token=get_bot_config().token)
    dp = Dispatcher()
    logging.basicConfig(level=logging.INFO)

    dp.include_router(group_emojies.router)
    dp.include_router(checkin.router)
    dp.include_router(usernames.router)
    dp.include_router(common.router)

    dp.callback_query.outer_middleware(WeekendCallbackMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("starting...")
    asyncio.run(main())
