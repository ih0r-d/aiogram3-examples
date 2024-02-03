import asyncio
import logging
from random import randint
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.filters.command import Command

from bots.config_reader import get_bot_config
from aiogram.types import BotCommand

bot_conf = get_bot_config()
bot = Bot(token=bot_conf.token)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Hello!, {message.from_user.first_name}")


@dp.message(Command("answer"))
async def cmd_answer(message: types.Message):
    await message.answer("Simple answer")


@dp.message(Command("reply"))
async def cmd_reply(message: types.Message):
    await message.reply('Reply answer')


@dp.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@dp.message(Command("add_to_list"))
async def cmd_add_to_list(message: types.Message, mylist: list[int]):
    num = randint(10, 100)
    mylist.append(num)
    await message.answer(f"Add number => {num}")


@dp.message(Command("info"))
async def cmd_info(message: types.Message, started_at: str):
    await message.answer(f"Bot started {started_at}")


async def cmd_show_list(message: types.Message, my_list: list[int]):
    await message.answer(f"Your data: {my_list}")


async def main():
    dp.message.register(cmd_show_list, Command("show_list"))

    commands = [
        BotCommand(command="start", description="Hello answer"),
        BotCommand(command="answer", description="Simple answer"),
        BotCommand(command="dice", description="Simple answer dice"),
        BotCommand(command="add_to_list", description="Add random number to list"),
        BotCommand(command="show_list", description="Show numbers list"),
        BotCommand(command="info", description="Show start bot time info")
    ]

    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, mylist=[1, 2, 3])


if __name__ == "__main__":
    asyncio.run(main())
