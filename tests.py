import asyncio

from src.models import Chat, ChatModerationLevelEnum
from src.services import MessageChecker
from src.services.check_is_message_from_bot import check_is_message_from_bot


class Tester:

    async def test_is_message_from_bot(self):
        assert await check_is_message_from_bot(
            None
        ) is False, 'без bot_via выдает, что это бот'

        assert await check_is_message_from_bot(
            'some_info'
        ) is True, 'не выдает что это бот, при передаче via_bot'

    async def set_up(self):
        self.bad_words = ['bad', 'gg', 'ver']
        MessageChecker.bad_words |= set(self.bad_words)

        self.chat_with_moder = Chat(
            moderation_level=ChatModerationLevelEnum.on.value,
            telegram_id=1,
            chat_name='2',
        )

        self.chat_without_moder = Chat(
            moderation_level=ChatModerationLevelEnum.off.value,
            telegram_id=2,
            chat_name='3',
        )

        self.good_texts = [
            'some text',
            f'{self.bad_words[0]}w',
            f'w{self.bad_words[0]}',
            '',
            'some text, s',
        ]

        self.bad_texts = [
            f'some world, '
            f'{self.bad_words[0]}-',
            f'{self.bad_words[1]}',
            f'{self.bad_words[2]},fewfw',
            f'some {self.bad_words[0]}',
        ]

    async def test_message_check_with_moder_level_good_words(self):
        chat = self.chat_with_moder

        for text in self.good_texts:
            assert MessageChecker(
                chat,
                text,
                True,
            ).check() is False, (
                    'moder_on,via_bot should be False | word: ' + text
            )
            assert MessageChecker(
                chat,
                text,
                False,
            ).check() is True, 'moder_on should be True | word: ' + text

    async def test_message_check_with_moder_level_bad_words(self):
        chat = self.chat_with_moder

        for text in self.bad_texts:
            assert MessageChecker(
                chat,
                text,
                True,
            ).check() is False, (
                    'moder_on,via_bot should be False | word: ' + text
            )
            assert MessageChecker(
                chat,
                text,
                False,
            ).check() is False, 'moder_on should be False | word: ' + text

    async def test_message_check_without_moder_level_good_words(self):
        chat = self.chat_without_moder

        for text in self.good_texts:
            assert MessageChecker(
                chat,
                text,
                True,
            ).check() is True, (
                    'moder_off,via_bot should be True | word: ' + text
            )
            assert MessageChecker(
                chat,
                text,
                False,
            ).check() is True, 'moder_off should be True | word: ' + text

    async def test_message_check_without_moder_level_bad_words(self):
        chat = self.chat_without_moder

        for text in self.bad_texts:
            assert MessageChecker(
                chat,
                text,
                True,
            ).check() is True, (
                    'moder_off,via_bot should be True | word: ' + text
            )
            assert MessageChecker(
                chat,
                text,
                False,
            ).check() is True, 'moder_off should be True | word: ' + text

    async def run(self):
        await self.set_up()

        for method_name in filter(lambda x: x.startswith('test_'),
                                  self.__dir__()):

            method = getattr(self, method_name)
            try:
                await method()
                print(f'{method_name} - OK')
            except AssertionError as ex:
                print(f'{method_name} - assertion error', ex)
                raise ex
            except Exception as ex:
                print(f'{method_name} - exception', ex)
                raise ex


if __name__ == '__main__':
    tester = Tester()
    asyncio.run(tester.run())
