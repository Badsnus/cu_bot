from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.chats import (
    GetLogsCallback,
)
from src.repo import DB
from src.services import send_logs

router: Router = Router()


@router.callback_query(GetLogsCallback.filter())
async def get_logs(call: CallbackQuery, callback_data: GetLogsCallback, db: DB) -> None:
    await send_logs(call, db, callback_data.id)
