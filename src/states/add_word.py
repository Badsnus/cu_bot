from aiogram.fsm.state import State, StatesGroup


class AddWordState(StatesGroup):
    word = State()
