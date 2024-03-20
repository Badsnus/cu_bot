from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.keyboards import word_back_menu, get_main_menu
from src.services import delete_word, get_or_create_user
from src.states import DeleteWordState

router: Router = Router()


@router.message((F.text == 'Удалить слово') & (F.chat.type == 'private'))
async def ask_word(message: Message, state: FSMContext) -> None:
    await message.answer(
        'Напиши слово для удаления',
        reply_markup=word_back_menu,
    )

    await state.set_state(DeleteWordState.word)


@router.message(DeleteWordState.word)
async def delete_world_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    user = await get_or_create_user(
        user_id=message.from_user.id,
    )

    if not user.is_admin:
        return

    if message.text == 'Отмена':
        await message.answer(
            'Ничего не удалил',
            reply_markup=get_main_menu(user.is_admin),
        )
        return

    is_deleted = await delete_word(message.text)

    text = 'Слово удалено' if is_deleted else 'Такого слова нет в бд'

    await message.answer(
        text,
        reply_markup=get_main_menu(user.is_admin),
    )
