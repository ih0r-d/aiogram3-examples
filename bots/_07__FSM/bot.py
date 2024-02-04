import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bots.config_reader import get_bot_config
from handlers import common, ordering_food, ordering_drinks
from aiogram.fsm.strategy import FSMStrategy


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.CHAT)
    bot = Bot(get_bot_config().token)

    dp.include_routers(common.router, ordering_food.router, ordering_drinks.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
