from re import findall

from src.models import Chat, ChatModerationLevelEnum

# todo офк надо отсюда вынести
bad_words = set(open('bad_words.txt', encoding='utf-8').read().splitlines())


class IsMessageGood:

    def __init__(self, chat: Chat, text: str, is_from_bot: bool) -> None:
        self._chat = chat
        self._text = text.lower()
        self._is_from_bot = is_from_bot

    def _is_bad_text(self) -> bool:
        words = set(findall(r'\w+', self._text))
        return bool(bad_words & words)

    def check(self) -> bool:
        if self._chat.moderation_level == ChatModerationLevelEnum.off.value:
            return True

        return not (self._is_bad_text() or self._is_from_bot)
