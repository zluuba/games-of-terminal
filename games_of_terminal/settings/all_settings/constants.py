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

MAX_USERNAME_LEN = 20

USERNAME_EDITING_MSGS = (
    'Enter new username and press Enter.',
    'To cancel editing and go back, press Esc.',
)

USERNAME_INVALID_MSGS = (
    'The username must contain at least one character.',
    'The changes have not been applied.',
)

USERNAME_VALID_MSGS = (
    'Changes have been applied.',
    'Interesting choice.',
    'I\'ll remember that.',
)

USERNAME_ALLOWED_CHARS = ascii_letters + digits + punctuation
USERNAME_COLOR_NAME = 'strong_pastel_purple_text_black_bg'


OPTIONS_CHOOSING_MSGS = (
    'Use the left and right arrows to scroll through the options.',
    'Press Enter to apply the selected option.',
)

OPTIONS_POST_MSG = 'Settings have been changed successfully.'
