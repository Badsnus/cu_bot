import asyncio

from src.models import Chat, ChatModerationLevelEnum
from src.services import MessageChecker
from src.services.check_is_message_from_bot import check_is_message_from_bot


class Tester:
    @staticmethod
    def parameterize(params: list[list]):
        def decorator(func):
            async def wrapper(*args2, **kwargs2):
                for param in params:
                    await func(*args2, *param, **kwargs2)

            return wrapper

        return decorator

    BAD_WORDS = ['bad', 'gg', 'ver']

    good_texts = [
        'some text',
        f'{BAD_WORDS[0]}w',
        f'w{BAD_WORDS[0]}',
        '',
        'some text, s',
    ]
    GOOD_TEXTS = [[text] for text in good_texts]

    bad_texts = BAD_WORDS + [
        f'some world, '
        f'{BAD_WORDS[0]}-',
        f'{BAD_WORDS[1]}',
        f'{BAD_WORDS[2]},fewfw',
        f'some {BAD_WORDS[0]}',
    ]
    BAD_TEXTS = [[text] for text in bad_texts]

    async def set_up(self):

        MessageChecker.bad_words |= set(self.BAD_WORDS)

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

    async def test_is_message_from_bot(self):
        assert await check_is_message_from_bot(
            None
        ) is False, 'без bot_via выдает, что это бот'

        assert await check_is_message_from_bot(
            'some_info'
        ) is True, 'не выдает что это бот, при передаче via_bot'

    @parameterize(GOOD_TEXTS)
    async def test_message_check_with_moderation_on_good_words(self,
                                                               text: str):
        chat = self.chat_with_moder

        assert MessageChecker(
            chat,
            text,
            True,
            is_from_channel=False,
        ).check() is False, (
                'moder_on,via_bot should be False | word: ' + text
        )
        assert MessageChecker(
            chat,
            text,
            False,
            is_from_channel=False,

        ).check() is True, 'moder_on should be True | word: ' + text

    @parameterize(BAD_TEXTS)
    async def test_message_check_with_moderation_on_bad_words(self,
                                                              text: str):
        chat = self.chat_with_moder

        assert MessageChecker(
            chat,
            text,
            True,
            is_from_channel=False,

        ).check() is False, (
                'moder_on,via_bot should be False | word: ' + text
        )
        assert MessageChecker(
            chat,
            text,
            False,
            is_from_channel=False,

        ).check() is False, 'moder_on should be False | word: ' + text

    @parameterize(GOOD_TEXTS)
    async def test_message_check_without_moderation_off_good_words(self,
                                                                   text: str):
        chat = self.chat_without_moder

        assert MessageChecker(
            chat,
            text,
            True,
            is_from_channel=False,

        ).check() is True, (
                'moder_off,via_bot should be True | word: ' + text
        )
        assert MessageChecker(
            chat,
            text,
            False,
            is_from_channel=False,

        ).check() is True, 'moder_off should be True | word: ' + text

    @parameterize(BAD_TEXTS)
    async def test_message_check_without_moderation_off_bad_words(self,
                                                                  text: str):
        chat = self.chat_without_moder

        assert MessageChecker(
            chat,
            text,
            True,
            is_from_channel=False,

        ).check() is True, (
                'moder_off,via_bot should be True | word: ' + text
        )
        assert MessageChecker(
            chat,
            text,
            False,
            is_from_channel=False,

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
