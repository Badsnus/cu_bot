from aiogram import Bot, Router
from aiogram.enums import ChatMemberStatus
from aiogram.types import ChatMemberUpdated

from src.repo import DB

router: Router = Router()


@router.chat_member()
async def edit_admins(chat_member_updated: ChatMemberUpdated, db: DB, bot: Bot) -> None:
    old = chat_member_updated.old_chat_member
    new = chat_member_updated.new_chat_member

    if old.status == ChatMemberStatus.MEMBER and new.status == ChatMemberStatus.ADMINISTRATOR:
        await db.chat.add_admin(new.user.id, chat_member_updated.chat.id, bot)
    elif old.status == ChatMemberStatus.ADMINISTRATOR and new.status != ChatMemberStatus.ADMINISTRATOR:
        await db.chat.delete_admin(new.user.id, chat_member_updated.chat.id)
