from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from src.repo import DB


class CheckAuthMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery | Message,
            data: Dict[str, Any],
    ) -> Any:
        db: DB = data.get('db')

        user = await db.user.get_by_tg_id(telegram_id=event.from_user.id)
        if not user:
            user = await db.user.create(event.from_user.id)
        data['user'] = user

        return await handler(event, data)
