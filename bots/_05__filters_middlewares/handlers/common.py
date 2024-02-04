from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def message_with_usernames(message: Message):
    await message.reply(
        f'Thank you for use this bot :)'
    )
