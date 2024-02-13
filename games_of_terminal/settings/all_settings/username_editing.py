from games_of_terminal.constants import KEYS, BASE_OFFSET, DEFAULT_COLOR
from games_of_terminal.database.database import get_username, save_username
from games_of_terminal.settings.all_settings.constants import (
    USERNAME_EDITING_MSGS, USERNAME_ALLOWED_CHARS,
    USERNAME_VALID_MSGS, USERNAME_INVALID_MSGS,
    USERNAME_COLOR_NAME,
)
from games_of_terminal.utils import (
    draw_message, clear_field_line,
    get_color_by_name, draw_colorful_message,
    show_cursor, hide_cursor,
)

from curses import A_BOLD as BOLD
from random import choice
from time import sleep


class UsernameEditing:
    def __init__(self, parent_class):
        self.parent_class = parent_class

        self.current_username = get_username()
        self.new_username = ''
        self.text_start_y = self.get_text_start_y()
        self.text_input_field_y = self.get_text_input_field_y()

    def get_text_start_y(self):
        return ((self.parent_class.height // 2) -
                ((len(USERNAME_EDITING_MSGS) + BASE_OFFSET + 1) // 2))

    def get_text_input_field_y(self):
        return self.text_start_y + len(USERNAME_EDITING_MSGS) + BASE_OFFSET

    def get_text_input_field_x(self):
        return (self.parent_class.width // 2) - (len(self.new_username) // 2)

    def run(self):
        self.parent_class.window.clear()
        self.draw_editing_window_text()
        self.draw_text_input_field()

        while True:
            key = self.parent_class.window.getch()
            self.parent_class.wait_for_keypress()

            if key == KEYS['escape']:
                return
            elif key in KEYS['enter']:
                hide_cursor()
                self.save_changes()
                self.draw_post_editing_text()
                return
            elif key in KEYS['delete']:
                self.handle_char_deleting()
            else:
                self.handle_char_adding(key)

            self.draw_text_input_field()

    def validate_new_username(self):
        username = self.new_username.replace(' ', '')

        if not username:
            return False
        return True

    def save_changes(self):
        if not self.validate_new_username():
            return
        if self.current_username == self.new_username:
            return

        save_username(self.new_username)

    def draw_post_editing_text(self):
        self.parent_class.window.clear()
        is_username_valid = self.validate_new_username()

        if is_username_valid:
            message = choice(USERNAME_VALID_MSGS)
            messages = (message.replace('<USERNAME>', self.new_username),)
        else:
            messages = USERNAME_INVALID_MSGS

        begin_y = (self.parent_class.height // 2) - (len(messages) // 2)

        for row, message in enumerate(messages):
            y = begin_y + row
            x = (self.parent_class.width // 2) - (len(message) // 2)

            draw_message(y, x, self.parent_class.window, message)

        sleep(2)

    def handle_char_adding(self, key):
        char = chr(key)

        if char not in USERNAME_ALLOWED_CHARS + ' ' + '.':
            return
        elif len(char) > 1:
            return

        self.new_username += char

    def handle_char_deleting(self):
        text_input_field_x = self.get_text_input_field_x()
        clear_field_line(self.text_input_field_y, text_input_field_x,
                         self.parent_class.window, len(self.new_username))
        self.new_username = self.new_username[:-1]

    def draw_text_input_field(self):
        text_input_field_x = self.get_text_input_field_x()
        draw_message(self.text_input_field_y, text_input_field_x,
                     self.parent_class.window, self.new_username,
                     DEFAULT_COLOR + BOLD)

        self.show_cursor()

    def show_cursor(self):
        x = self.get_text_input_field_x() + len(self.new_username)
        self.parent_class.window.move(self.text_input_field_y, x)
        show_cursor()

    def draw_editing_window_text(self):
        self.show_current_username()

        for row, message in enumerate(USERNAME_EDITING_MSGS):
            y = self.text_start_y + row
            x = (self.parent_class.width // 2) - (len(message) // 2)

            draw_message(y, x, self.parent_class.window, message)

    def show_current_username(self):
        y = self.text_start_y - BASE_OFFSET
        text = self.get_current_username_text()

        draw_colorful_message(y, self.parent_class.width,
                              self.parent_class.window, text)

    def get_current_username_text(self):
        if self.current_username:
            username_color = get_color_by_name(USERNAME_COLOR_NAME)
            return (
                ('Current username is ', DEFAULT_COLOR),
                (self.current_username, username_color),
                ('.', DEFAULT_COLOR),
            )
        return (('The username is not set.', DEFAULT_COLOR),)
