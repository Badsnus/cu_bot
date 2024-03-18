from aiogram import Bot, F, Router, types

from src.repo import DB
from src.services import update_chat_info

router: Router = Router()


@router.message(F.chat.type != 'private')
async def on_admin_change(message: types.Message, db: DB, bot: Bot) -> None:
    await update_chat_info(message, db, bot)
