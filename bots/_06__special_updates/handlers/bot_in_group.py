import logging

from aiogram import F, Router, Bot
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))

chats_variants = {
    "group": "Group",
    "supergroup": "Super group"
}


# todo: Could not reproduce the case of adding a bot as Restricted, therefore there will be no example with it

@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated):
    # todo: The simplest case: the bot is added as an admin. We can easily send a message
    await event.answer(
        text=f"Hi! Thanks for adding me to "
             f'{chats_variants[event.chat.type]} "{event.chat.title}"'
             f"as administrator. Chat ID: {event.chat.id}"
    )


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    # todo: A more complicated option: the bot was added as a regular participant.
    #  But you may not have the right to write messages, so let's check in advance.
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await event.answer(
            text=f"Hi! Thanks for adding me to "
                 f'{chats_variants[event.chat.type]} "{event.chat.title}"'
                 f"as a regular participant. Chat ID: {event.chat.id}"
        )
    else:
        logging.log("We will log this situation somehow")
