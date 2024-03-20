from re import findall

from src.models import Chat, ChatModerationLevelEnum


class IsMessageGood:
    bad_words: set = set()

    def __init__(self, chat: Chat, text: str, is_from_bot: bool) -> None:
        self._chat = chat
        self._text = text.lower()
        self._is_from_bot = is_from_bot

    def _is_bad_text(self) -> bool:
        words = set(findall(r'\w+', self._text))
        print(self.bad_words)
        return bool(self.bad_words & words)

    def check(self) -> bool:
        if self._chat.moderation_level == ChatModerationLevelEnum.off.value:
            return True

        return not (self._is_bad_text() or self._is_from_bot)
