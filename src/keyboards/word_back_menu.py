from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

word_back_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Отмена'),
    ],
])
