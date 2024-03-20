from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu(is_admin: bool) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
                     [
                         KeyboardButton(text='Добавленные чаты'),
                     ],
                 ] + [
                     [
                         KeyboardButton(text='Добавить слово'),
                         KeyboardButton(text='Удалить слово'),
                     ] if is_admin
                     else []
                 ]
    )
