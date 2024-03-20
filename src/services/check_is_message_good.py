from re import findall

from src.models import Chat, ChatModerationLevelEnum

# todo офк надо отсюда вынести
bad_words = set(open('bad_words.txt', encoding='utf-8').read().splitlines())


def is_bad_text(text: str) -> bool:
    words = set(findall(r'\w+', text.lower()))
    return bool(bad_words & words)


async def check_is_message_good(chat: Chat,
                                text: str,
                                is_from_bot: bool) -> bool:
    if chat.moderation_level == ChatModerationLevelEnum.off.value:
        return True

    return not (is_bad_text(text) or is_from_bot)
