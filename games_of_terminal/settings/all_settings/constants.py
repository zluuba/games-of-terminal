from string import ascii_letters, digits, punctuation
from random import choice


TITLE = [
    '╔═╗╔═╗╔╦╗╔╦╗╦╔╗╔╔═╗╔═╗',
    '╚═╗║╣  ║  ║ ║║║║║ ╗╚═╗',
    '╚═╝╚═╝ ╩  ╩ ╩╚╚╝╚═╝╚═╝',
]

LEFT_ARROW = '<'
RIGHT_ARROW = '>'
UPWARDS_ARROW = '▲'
DOWNWARDS_ARROW = '▼'
NO_ARROW = ' '

TOP_OFFSET = 2
BOTTOM_OFFSET = 2
SIDE_ARROW_OFFSET = 4

USERNAME_EDITING_MSGS = (
    'Enter new username and press Enter.',
    'To cancel editing and go back, press Esc.',
)

USERNAME_INVALID_MSGS = (
    'The username must contain at least one character.',
    'The changes have not been applied.',
)

USERNAME_VALID_MSGS = (
    '<USERNAME>? Is that your real name? Lmao',
    'Changes have been applied.',
    'Henceforth I name you <USERNAME>.',
    'Hi, <USERNAME>. How you doin\'? ;)',
    'Interesting choice.',
    'Username with Twitter vibes, nice work.',
    'So, you really want to be called <USERNAME>? Okay..',
    'Username <<USERNAME>> was successfully saved.',
)

USERNAME_ALLOWED_CHARS = ascii_letters + digits + punctuation
USERNAME_COLOR_NAME = 'strong_pastel_purple_text_black_bg'
