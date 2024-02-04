import asyncio
import logging

from aiogram import Bot, Dispatcher, html, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile
from aiogram.utils.formatting import as_list, as_marked_section, Bold, as_key_value, HashTag
from aiogram.utils.markdown import hide_link
from aiogram.utils.media_group import MediaGroupBuilder

from bots.config_reader import get_bot_config

bot_conf = get_bot_config()
bot = Bot(token=bot_conf.token, parse_mode="HTML")

dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def any_message(message: Message):
    await message.answer("Hello, <b>world</b>!", parse_mode=ParseMode.HTML)
    await message.answer("Hello, *world*\!", parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer("Message with  <u>HTML-template</u>")
    await message.answer("Message without <s>marking</s>", parse_mode=None)


@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
        parse_mode=ParseMode.HTML
    )


@dp.message(Command("advanced_example"))
async def cmd_advanced_example(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 3",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 2",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 4),
            as_key_value("Success", 3),
            as_key_value("Failed", 1),
            marker="  ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())


@dp.message(Command("set_timer"))
async def cmd_set_timer(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Error: Not available input arguments"
        )
        return
    try:
        delay_time, text_to_send = command.args.split(" ", maxsplit=1)
    except ValueError:
        await message.answer(
            "Error: wrong command format . Example:\n"
            "/set_timer <time> <message>"
        )
        return
    await message.answer(
        "Timer added!\n"
        f"Time: {delay_time}\n"
        f"Message: {text_to_send}"
    )


@dp.message(Command("custom1", prefix="%"))
async def cmd_custom1(message: Message):
    await message.answer("Custom command 1!")


@dp.message(Command("help"))
@dp.message(CommandStart(
    deep_link=True, magic=F.args == "help"
))
async def cmd_start_help(message: Message):
    await message.answer("Message with help")


@dp.message(Command("hidden_link"))
async def cmd_hidden_link(message: Message):
    await message.answer(
        f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
    )


@dp.message(Command('images'))
async def upload_photo(message: Message):
    file_ids = []

    with open("img_1.png", "rb") as buff:
        result = await message.answer_photo(
            BufferedInputFile(
                buff.read(),
                filename="img_1.png"
            ),
            caption="Buffer image 1"
        )
        file_ids.append(result.photo[-1].file_id)

    image_from_pc = FSInputFile("img_2.png")
    result = await message.answer_photo(
        image_from_pc,
        caption="Image from PC"
    )
    file_ids.append(result.photo[-1].file_id)

    image_from_url = URLInputFile("https://picsum.photos/seed/qqq/400/300")
    result = await message.answer_photo(
        image_from_url,
        caption="Image"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Sent files:\n" + "\n".join(file_ids))


@dp.message(Command("album"))
async def cmd_album(message: Message):
    album_builder = MediaGroupBuilder(
        caption="General signature for the future album"
    )
    album_builder.add(
        type="photo",
        media=FSInputFile("img_1.png")

    )
    album_builder.add_photo(
        media="https://picsum.photos/200/300"
    )
    album_builder.add_photo(
        media="AgACAgIAAxkDAAM5ZY7XOBKopB9wct73n9rstCXGIF8AAoXVMRvMTnhI88jxz6CljdsBAAMCAAN4AAM0BA"
    )
    await message.answer_media_group(
        media=album_builder.build()
    )


@dp.message(F.text)
async def extract_data(message: Message):
    await message.reply(f"Not supported command => {message.text}")


@dp.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)


@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    await bot.download(
        message.photo[-1],
        destination=f"/tmp/{message.photo[-1].file_id}.jpg"
    )


@dp.message(F.sticker)
async def download_sticker(message: Message, bot: Bot):
    await bot.download(
        message.sticker,
        destination=f"/tmp/{message.sticker.file_id}.webp"
    )


@dp.message(F.new_chat_members)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        await message.reply(f"Hi, {user.full_name}")


@dp.message(F.text)
async def extract_data(message: Message):
    await message.reply(f"Not supported command => {message.text}")


async def main():
    await bot.delete_my_commands()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
