from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED, LEFT, \
    RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR
from aiogram.types import ChatMemberUpdated

from bots.config_reader import get_bot_config

router = Router()
router.chat_member.filter(F.chat.id == get_bot_config().chat_group_id)


# https://docs.aiogram.dev/en/latest/dispatcher/filters/chat_member_updated.html#transitions

@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=(KICKED | LEFT | RESTRICTED | MEMBER) >> (ADMINISTRATOR | CREATOR)
    )
)
async def admin_promoted(event: ChatMemberUpdated, admins: set[int]):
    admins.add(event.new_chat_member.user.id)
    await event.answer(f"{event.new_chat_member.user.first_name} was promoted to Administrator!")


@router.chat_member(
    ChatMemberUpdatedFilter(
        # Pay attention to the direction of the arrows Or you could swap the objects in the brackets
        member_status_changed=(KICKED | LEFT | RESTRICTED | MEMBER) << (ADMINISTRATOR | CREATOR)
    )
)
async def admin_demoted(event: ChatMemberUpdated, admins: set[int]):
    admins.discard(event.new_chat_member.user.id)
    await event.answer(f"{event.new_chat_member.user.first_name} was demoted to a regular user!")
