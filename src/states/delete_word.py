from aiogram.fsm.state import State, StatesGroup


class DeleteWordState(StatesGroup):
    word = State()
