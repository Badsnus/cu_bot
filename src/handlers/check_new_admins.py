from aiogram import Router
from aiogram.types import ChatMemberUpdated

from src.services import update_admin_status

router: Router = Router()


@router.chat_member()
async def edit_admins(update: ChatMemberUpdated) -> None:
    await update_admin_status(
        user_id=update.new_chat_member.user.id,
        chat_id=update.chat.id,
        old_status=update.old_chat_member.status,
        new_status=update.new_chat_member.status,
    )
