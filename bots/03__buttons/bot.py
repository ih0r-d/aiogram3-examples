import asyncio
import logging
from contextlib import suppress
from random import randint
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bots.config_reader import get_bot_config

bot_conf = get_bot_config()
bot = Bot(token=bot_conf.token, parse_mode="HTML")

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

user_data = {}

GREEN_TEA = 'Green tea'
BLACK_TEA = 'Black tea with milk'


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text=GREEN_TEA),
            types.KeyboardButton(text=BLACK_TEA)
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Which tea will you choose?"
    )
    await message.answer("What tea will you drink?", reply_markup=keyboard)


@dp.message(F.text == GREEN_TEA)
async def with_puree(message: types.Message):
    await message.reply("It is really tasty.", reply_markup=types.ReplyKeyboardRemove())


@dp.message(F.text == BLACK_TEA)
async def without_puree(message: types.Message):
    await message.reply("Not good for me.", reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command("reply_builder"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Choose a number:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Request geolocation", request_location=True),
        types.KeyboardButton(text="Request contact", request_contact=True)
    )
    builder.row(types.KeyboardButton(
        text="Create a quiz",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    builder.row(
        types.KeyboardButton(
            text="Select premium user",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Select a supergroup with forums",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )

    await message.answer(
        "Choose an action:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.user_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )


@dp.message(F.chat_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.chat_shared.request_id}. "
        f"User ID: {message.chat_shared.chat_id}"
    )


@dp.message(Command("inline_url"))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com/ih0r-d/aiogram3-examples")
    )
    builder.row(types.InlineKeyboardButton(
        text="Official Telegram channel",
        url="tg://resolve?domain=telegram")
    )

    user_id = message.from_user.id
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Some user",
            url=f"tg://user?id={user_id}")
        )
    await message.answer(
        'Please, choose a link?',
        reply_markup=builder.as_markup(),
    )


@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Click me",
        callback_data="random_value")
    )
    await message.answer(
        "Click button to return some random number.",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 10)))
    await callback.answer(
        text="Thank you for using the bot!",
        show_alert=True
    )
    # or await call.answer()


# ----------
# Without factory
def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(text="Approve", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Enter the number: {new_value}",
            reply_markup=get_keyboard()
        )


@dp.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Enter the number: 0", reply_markup=get_keyboard())


@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value + 1
        await update_num_text(callback.message, user_value + 1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value - 1
        await update_num_text(callback.message, user_value - 1)
    elif action == "finish":
        await callback.message.edit_text(f"Result: {user_value}")

    await callback.answer()


# ----------
# With factory
class NumbersCallbackFactory(CallbackData, prefix="fab_num"):
    action: str
    value: Optional[int] = None


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(text="-2", callback_data=NumbersCallbackFactory(action="change", value=-2))
    builder.button(text="-1", callback_data=NumbersCallbackFactory(action="change", value=-1))
    builder.button(text="+1", callback_data=NumbersCallbackFactory(action="change", value=1))
    builder.button(text="+2", callback_data=NumbersCallbackFactory(action="change", value=2))
    builder.button(text="Confirm", callback_data=NumbersCallbackFactory(action="finish"))
    builder.adjust(4)
    return builder.as_markup()


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Enter the number: {new_value}",
            reply_markup=get_keyboard_fab()
        )


@dp.message(Command("numbers_fab"))
async def cmd_numbers_fab(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Enter the number: 0", reply_markup=get_keyboard_fab())


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callbacks_num_change_fab(callback: types.CallbackQuery, callback_data: NumbersCallbackFactory):
    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text_fab(callback.message, user_value + callback_data.value)
    await callback.answer()


@dp.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f"Result: {user_value}")
    await callback.answer()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
