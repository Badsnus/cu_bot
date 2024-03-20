import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config.config import load_test_database_url
from src.models import Base, Chat, ChatModerationLevelEnum, Log, User, UserChat
from src.repo import DB
from src.services import update_chat_info


class MockUser:
    def __init__(self, id: int) -> None:
        self.id = id


class MockAdmin:

    def __init__(self, user_id: int) -> None:
        self.user = MockUser(user_id)


class Tester:

    def __init__(self):
        db_connection = load_test_database_url()

        self._db_engine = create_async_engine(
            url=db_connection,
            echo=False,
        )
        self._db_session_maker = async_sessionmaker(
            self._db_engine,
            expire_on_commit=False,
        )

    async def configurate_db(self):
        async with self._db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    async def test_update_chat_info_create_chat(self, db: DB) -> None:
        chat_id = 1
        chat_name = 'chat_name'
        bot_id = 3
        admins = [MockAdmin(1), MockAdmin(2), MockAdmin(bot_id)]
        chat = await db.chat.get(chat_id)

        assert chat is None

        chat = await update_chat_info(chat_id, chat_name, admins, bot_id, db)

        assert isinstance(chat, Chat)
        assert chat.telegram_id == chat_id
        assert chat.chat_name == chat_name
        assert chat.moderation_level == ChatModerationLevelEnum.on.value

        chat_clone = await db.chat.get(chat.telegram_id)
        assert chat_clone == chat

        admins = db.chat.get_chats_by_user()

    async def run(self):
        for method_name in filter(lambda x: x.startswith('test_'),
                                  self.__dir__()):
            await self.configurate_db()
            method = getattr(self, method_name)
            try:
                async with self._db_session_maker() as session:
                    await method(DB(session))
                print(f'{method_name} - OK')
            except AssertionError as ex:
                print(f'{method_name} - assertion error', ex)
            except Exception as ex:
                print(f'{method_name} - exception', ex)


if __name__ == '__main__':
    tester = Tester()
    asyncio.run(tester.run())
