from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
         Creates a replay keyboard with buttons in one row
         :param items: list of texts for buttons
         :return: replay keyboard object
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
