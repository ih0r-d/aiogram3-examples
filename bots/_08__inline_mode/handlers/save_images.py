from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize, \
    InlineKeyboardMarkup, InlineKeyboardButton

from bots._08__inline_mode.states import SaveCommon
from bots._08__inline_mode.storage import add_photo

router = Router()


@router.message(SaveCommon.waiting_for_save_start, F.photo[-1].as_("photo"))
async def save_image(message: Message, photo: PhotoSize, state: FSMContext):
    add_photo(message.from_user.id, photo.file_id, photo.file_unique_id)
    await state.clear()
    kb = [[InlineKeyboardButton(text="Try it", switch_inline_query="images")]]
    await message.answer(text="Image saved!", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))
