import asyncio

from src.models import Chat, ChatModerationLevelEnum
from src.services.check_is_message_from_bot import check_is_message_from_bot
from src.services import MessageChecker


class Tester:

    async def test_is_message_from_bot(self):
        assert await check_is_message_from_bot(None) is False, 'без bot_via выдает, что это бот'
        assert await check_is_message_from_bot('some_info') is True, 'не выдает что это бот, при передаче via_bot'

    async def test_message_check_with_moder_level(self):
        b_w = ['bad', 'gg', 'ver']
        MessageChecker.bad_words |= set(b_w)

        # CHAT MODERATION ON
        chat = Chat(moderation_level=ChatModerationLevelEnum.on.value, telegram_id=1, chat_name='2')

        texts_without_bad_words = ['some text', f'{b_w[0]}w', f'w{b_w[0]}', '', 'some text, s']
        for txt in texts_without_bad_words:
            assert MessageChecker(chat, txt, True).check() is False, 'moder_on,via_bot should be False | word: ' + txt
            assert MessageChecker(chat, txt, False).check() is True, 'moder_on should be True | word: ' + txt

        texts_with_bad_words = [f'some world, {b_w[0]}-', f'{b_w[1]}', f'{b_w[2]},fewfw', f'some {b_w[0]}']
        for txt in texts_with_bad_words:
            assert MessageChecker(chat, txt, True).check() is False, 'moder_on,via_bot should be False | word: ' + txt
            assert MessageChecker(chat, txt, False).check() is False, 'moder_on should be False | word: ' + txt

        # CHAT MODERATION OFF
        chat = Chat(moderation_level=ChatModerationLevelEnum.off.value, telegram_id=1, chat_name='2')

        texts_without_bad_words = ['some text', f'{b_w[0]}w', f'w{b_w[0]}', '', 'some text, s']
        for txt in texts_without_bad_words:
            assert MessageChecker(chat, txt, True).check() is True, 'moder_off,via_bot should be False | word: ' + txt
            assert MessageChecker(chat, txt, False).check() is True, 'moder_off should be True | word: ' + txt

        texts_with_bad_words = [f'some world, {b_w[0]}-', f'{b_w[1]}', f'{b_w[2]},fewfw', f'some {b_w[0]}']
        for txt in texts_with_bad_words:
            assert MessageChecker(chat, txt, True).check() is True, 'moder_off,via_bot should be False | word: ' + txt
            assert MessageChecker(chat, txt, False).check() is True, 'moder_off should be False | word: ' + txt

    async def run(self):
        for method_name in filter(lambda x: x.startswith('test_'),
                                  self.__dir__()):

            method = getattr(self, method_name)
            try:
                await method()
                print(f'{method_name} - OK')
            except AssertionError as ex:
                print(f'{method_name} - assertion error', ex)
            except Exception as ex:
                print(f'{method_name} - exception', ex)


if __name__ == '__main__':
    tester = Tester()
    asyncio.run(tester.run())
