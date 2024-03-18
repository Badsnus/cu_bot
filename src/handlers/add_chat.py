from aiogram import Bot, F, Router, types

from src.repo import DB

router: Router = Router()


@router.message(F.chat.type == 'private')
async def on_admin_change(message: types.Message, db: DB) -> None:
    print(message)


@router.message()
async def on_admin_change(message: types.Message, db: DB) -> None:
    print(message.chat.id)
