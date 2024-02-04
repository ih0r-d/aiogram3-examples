import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import in_pm, bot_in_group, group_admins, group_events
from bots.config_reader import get_bot_config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher()
    bot = Bot(get_bot_config().token, parse_mode="HTML")
    dp.include_routers(
        in_pm.router, events_in_group.router,
        bot_in_group.router, admin_changes_in_group.router
    )

    admins = await bot.get_chat_administrators(get_bot_config().chat_group_id)
    admin_ids = {admin.user.id for admin in admins}

    await dp.start_polling(bot, admins=admin_ids)


if __name__ == '__main__':
    asyncio.run(main())
