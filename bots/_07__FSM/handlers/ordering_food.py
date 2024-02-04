from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from bots._07__FSM.keyboards.simple_row import make_row_keyboard

router = Router()

available_food_names = ["Sushi", "Spaghetti", "Khachapuri"]
available_food_sizes = ["Small", "Medium", "Large"]


class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()


@router.message(StateFilter(None), Command("food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Choose a dish:",
        reply_markup=make_row_keyboard(available_food_names)
    )
    await state.set_state(OrderFood.choosing_food_name)


@router.message(OrderFood.choosing_food_name, F.text.in_(available_food_names))
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Thank you. Now please select your serving size:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)


# todo: In general, no one bothers to specify states entirely in strings
@router.message(StateFilter("OrderFood:choosing_food_name"))
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know such a dish.\n\nPlease select one of the titles from the list below:",
        reply_markup=make_row_keyboard(available_food_names)
    )


@router.message(OrderFood.choosing_food_size, F.text.in_(available_food_sizes))
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(
        text=f"You have selected {message.text.lower()} portion {user_data['chosen_food']}.\n"
             f"Try ordering drinks now: /drinks",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know this portion size.\n\n"
             "Please select one of the options from the list below:",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
