import asyncio

from aiogram import Bot, Dispatcher

from bots.config_reader import get_bot_config
from questions import router as questions_router
from different_types import router as different_types_router


async def main():
    bot = Bot(token=get_bot_config().token)
    dp = Dispatcher()

    dp.include_routers(questions_router, different_types_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("starting...")
    asyncio.run(main())
