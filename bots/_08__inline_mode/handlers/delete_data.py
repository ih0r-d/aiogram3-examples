from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bots._08__inline_mode.filters import HasLinkFilter, ViaBotFilter
from bots._08__inline_mode.states import DeleteCommon
from bots._08__inline_mode.storage import delete_link, delete_image

router = Router()


@router.message(DeleteCommon.waiting_for_delete_start, F.text, ViaBotFilter(), HasLinkFilter())
async def link_deletion_handler(message: Message, link: str, state: FSMContext):
    delete_link(message.from_user.id, link)
    await state.clear()
    await message.answer(text="Link deleted! The online mode output will be updated within a few minutes.")


@router.message(DeleteCommon.waiting_for_delete_start, F.photo[-1].file_unique_id.as_("file_unique_id"), ViaBotFilter())
async def image_deletion_handler(message: Message, state: FSMContext, file_unique_id: str):
    delete_image(message.from_user.id, file_unique_id)
    await state.clear()
    await message.answer(text="Image deleted! The online mode output will be updated within a few minutes.")
