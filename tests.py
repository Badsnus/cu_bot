import asyncio

from src.services.check_is_message_from_bot import check_is_message_from_bot


class Tester:

    async def test_is_message_from_bot(self):
        assert await check_is_message_from_bot(None) is False
        assert await check_is_message_from_bot('some_info') is True

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
