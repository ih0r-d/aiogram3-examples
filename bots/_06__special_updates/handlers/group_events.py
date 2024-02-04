from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import Message

router = Router()


# todo:
#  Then all handlers in the router will be automatically called
#  only for people from admins, this will shorten the bots and eliminate unnecessary if
#  but for example, we’ll do it using if-else to make it clearer
@router.message(Command("ban"), F.reply_to_message)
async def cmd_ban(message: Message, admins: set[int]):
    if message.from_user.id not in admins:
        await message.answer("You do not have sufficient rights to perform this action")
    else:
        await message.chat.ban(user_id=message.reply_to_message.from_user.id)
        await message.answer("User blocked")
