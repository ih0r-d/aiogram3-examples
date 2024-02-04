from typing import List

from aiogram import Router, F
from aiogram.types import Message

from bots._05__filters_middlewares.filters.username import HasUsernamesFilter

router = Router()


@router.message(F.text, HasUsernamesFilter())
async def message_with_usernames(message: Message, usernames: List[str]):
    await message.reply(
        f'Thank you! I will definitely subscribe to '
        f'{", ".join(usernames)}'
    )
