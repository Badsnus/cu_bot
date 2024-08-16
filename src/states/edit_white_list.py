from aiogram.fsm.state import State, StatesGroup


class EditWhiteList(StatesGroup):
    file = State()
