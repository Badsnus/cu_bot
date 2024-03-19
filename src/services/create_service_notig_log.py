from datetime import datetime

from src.repo import DB


async def create_chat_member_log(chat_id: int,
                                 chat_name: str,
                                 message_time: datetime,
                                 member_user_id: int,
                                 member_user_name: str,
                                 text: str,
                                 db: DB) -> None:
    await db.log.create(
        chat_id=chat_id,
        user_id=member_user_id,
        message='[ServiceMessage]' + text,
        time=message_time,
        chat_name=chat_name,
        user_name=member_user_name,
    )


async def create_member_leave_log(chat_id: int,
                                  chat_name: str,
                                  message_time: datetime,
                                  member_user_id: int,
                                  member_user_name: str,
                                  from_user_id: int,
                                  from_user_username: str,
                                  db: DB) -> None:
    text = 'user leave' if member_user_id == from_user_id else f'user kicked by {from_user_username}'

    await create_chat_member_log(
        chat_id=chat_id,
        chat_name=chat_name,
        message_time=message_time,
        member_user_id=member_user_id,
        member_user_name=member_user_name,
        text=text,
        db=db
    )


async def create_member_join_log(chat_id: int,
                                 chat_name: str,
                                 message_time: datetime,
                                 member_user_id: int,
                                 member_user_name: str,
                                 from_user_id: int,
                                 from_user_username: str,
                                 db: DB) -> None:
    text = 'user join' if member_user_id == from_user_id else f'user added by {from_user_username}'

    await create_chat_member_log(
        chat_id=chat_id,
        chat_name=chat_name,
        message_time=message_time,
        member_user_id=member_user_id,
        member_user_name=member_user_name,
        text=text,
        db=db
    )
