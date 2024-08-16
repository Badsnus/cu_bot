from string import ascii_lowercase, digits
from random import choices


def generate_invite_code(length: int = 10) -> str:
    return ''.join(choices(ascii_lowercase + digits, k=length))
