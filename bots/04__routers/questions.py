from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="yes")
    kb.button(text="no")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Do you like your current project ?",
        reply_markup=get_yes_no_kb()
    )


@router.message(F.text.lower() == "yes")
async def answer_yes(message: Message):
    await message.answer(
        "Mostly yes",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "no")
async def answer_no(message: Message):
    await message.answer(
        "Not sure...",
        reply_markup=ReplyKeyboardRemove()
    )
