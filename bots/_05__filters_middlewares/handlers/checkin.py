from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bots._05__filters_middlewares.keyboards.checkin import get_checkin_kb
from bots._05__filters_middlewares.middlewares.weekend import WeekendMessageMiddleware

router = Router()
router.message.filter(F.chat.type == "private")
router.message.middleware(WeekendMessageMiddleware())


@router.message(Command("checkin"))
async def cmd_checkin(message: Message):
    await message.answer(
        "Please click on the button below:",
        reply_markup=get_checkin_kb()
    )


@router.callback_query(F.data == "confirm")
async def checkin_confirm(callback: CallbackQuery):
    await callback.answer(
        "Thank you, confirmed!",
        show_alert=True
    )
