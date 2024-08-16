from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import ChatJoinRequest

from src.services.check_can_user_join import check_can_user_join

router = Router()


@router.chat_join_request()
async def handle_user_joining_via_invite_link(request: ChatJoinRequest, bot: Bot) -> None:
    link_name = request.invite_link.name
    user = request.from_user
    chat = request.chat

    if user.username != link_name:
        await request.answer_pm('<b>Это не ваша ссылка для вступления.\n\n</b>'
                                '<code>Перейдите по той ссылке, которую получали'
                                'вы и получите в боте персональную ссылку.</code>')
        return

    can_user_join = await check_can_user_join(chat.id, chat.type != 'channel', user.username, user.id)

    if not can_user_join:
        await request.answer_pm('<b>С этого юзернейма уже зашел другой пользователь.'
                                'Или вас исключили из списков\n\n</b>'
                                '<code>Если вы считаете, что это ошибка - напишите администратору.</code>')
        return

    await request.approve()
