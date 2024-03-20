from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards import add_word_menu, get_main_menu
from src.services import get_or_create_user, create_word
from src.states import AddWordState

router: Router = Router()


@router.message((F.text == 'Добавить слово') & (F.chat.type == 'private'))
async def ask_word(message: Message, state: FSMContext) -> None:
    await message.answer(
        'Напиши слово для добавление',
        reply_markup=add_word_menu,
    )

    await state.set_state(AddWordState.word)


@router.message(AddWordState.word)
async def add_word(message: Message, state: FSMContext) -> None:
    await state.clear()

    user = await get_or_create_user(
        user_id=message.from_user.id,
    )

    if not user.is_admin:
        return

    if message.text == 'Отмена':
        await message.answer(
            'Не добавляю',
            reply_markup=get_main_menu(user.is_admin),
        )
        return

    await create_word(message.text)

    await message.answer(
        'Слово добавлено',
        reply_markup=get_main_menu(user.is_admin),
    )
