from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

add_word_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Отмена'),
    ],
])
