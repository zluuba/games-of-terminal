from games_of_terminal.constants import KEYS, BASE_OFFSET, DEFAULT_COLOR
from games_of_terminal.database.database import get_username, save_username
from games_of_terminal.interface_manager import InterfaceManager
from games_of_terminal.settings.all_settings.constants import (
    USERNAME_EDITING_MSGS, USERNAME_ALLOWED_CHARS,
    USERNAME_VALID_MSGS, USERNAME_INVALID_MSGS,
    USERNAME_COLOR_NAME, MAX_USERNAME_LEN,
)
from games_of_terminal.utils import (
    draw_message, clear_field_line,
    get_color_by_name, draw_colorful_message,
    show_cursor, hide_cursor,
)

from curses import flushinp, A_BOLD as BOLD
from random import choice
from time import sleep


class UsernameEditing(InterfaceManager):
    def __init__(self, canvas):
        super().__init__(canvas, only_main_win=True)

        self.current_username = get_username()
        self.new_username = ''
        self.setup_vars()

    def setup_vars(self):
        self.height, self.width = self.canvas.getmaxyx()

        self.text_start_y = self.get_text_start_y()
        self.text_input_field_y = self.get_text_input_field_y()
        self.too_many_characters_msg_y = self.text_input_field_y + BASE_OFFSET

        self.max_username_length = 20

    def get_text_start_y(self):
        return ((self.height // 2) -
                ((len(USERNAME_EDITING_MSGS) + BASE_OFFSET + 1) // 2))

    def get_text_input_field_y(self):
        return self.text_start_y + len(USERNAME_EDITING_MSGS) + BASE_OFFSET

    def get_text_input_field_x(self):
        return (self.width // 2) - (len(self.new_username) // 2)

    def run(self):
        self.draw_username_editing_window()

        while True:
            key = self.window.getch()
            self.wait_for_keypress()

            if key == KEYS['escape']:
                hide_cursor()
                return
            elif key == KEYS['resize']:
                self.window.timeout(0)
                self.resize_menu_win_handler(key)
            elif key in KEYS['enter']:
                self.handle_username_saving()
                return
            elif key in KEYS['delete']:
                self.handle_char_deleting()
            else:
                self.handle_char_adding(key)

            self.draw_text_input_field()

    def draw_username_editing_window(self):
        self.window.clear()
        self.show_current_username()
        self.draw_tips_text()
        self.draw_text_input_field()

    def handle_username_saving(self):
        hide_cursor()
        self.save_changes()
        self.draw_post_editing_text()

    def validate_new_username(self):
        username = self.new_username.strip()

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
        self.window.clear()
        is_username_valid = self.validate_new_username()

        if is_username_valid:
            messages = (choice(USERNAME_VALID_MSGS),)
        else:
            messages = USERNAME_INVALID_MSGS

        begin_y = (self.height // 2) - (len(messages) // 2)

        for row, message in enumerate(messages):
            y = begin_y + row
            x = (self.width // 2) - (len(message) // 2)

            draw_message(y, x, self.window, message)

        sleep(2)

    def handle_char_adding(self, key):
        try:
            char = chr(key)
        except ValueError:
            return

        if char not in USERNAME_ALLOWED_CHARS + ' ' + '.':
            return
        elif len(char) > 1:
            return
        elif len(self.new_username) >= 20:
            self.show_too_many_characters_msg()
            return

        self.new_username += char

    def show_too_many_characters_msg(self):
        hide_cursor()
        color = get_color_by_name('strong_red_text_black_bg')
        message = f'Username can contain {MAX_USERNAME_LEN} characters maximum.'
        y = self.too_many_characters_msg_y
        x = (self.width // 2) - (len(message) // 2)

        draw_message(y, x, self.window, message, color)
        sleep(1)

        clear_field_line(y, x, self.window, len(message))
        show_cursor()
        flushinp()

    def handle_char_deleting(self):
        text_input_field_x = self.get_text_input_field_x()
        clear_field_line(self.text_input_field_y, text_input_field_x,
                         self.window, len(self.new_username))
        self.new_username = self.new_username[:-1]

    def draw_text_input_field(self):
        text_input_field_x = self.get_text_input_field_x()
        draw_message(self.text_input_field_y, text_input_field_x,
                     self.window, self.new_username,
                     DEFAULT_COLOR + BOLD)

        self.show_cursor()

    def show_cursor(self):
        x = self.get_text_input_field_x() + len(self.new_username)
        self.window.move(self.text_input_field_y, x)
        show_cursor()

    def draw_tips_text(self):
        color = get_color_by_name('grey_text_black_bg')

        for row, message in enumerate(USERNAME_EDITING_MSGS):
            y = self.text_start_y + row
            x = (self.width // 2) - (len(message) // 2)

            draw_message(y, x, self.window, message, color)

    def show_current_username(self):
        y = self.text_start_y - BASE_OFFSET
        text = self.get_current_username_text()

        draw_colorful_message(y, self.width, self.window, text)

    def get_current_username_text(self):
        if self.current_username:
            username_color = get_color_by_name(USERNAME_COLOR_NAME)
            return (('Current username is ', DEFAULT_COLOR),
                    (self.current_username, username_color),
                    ('.', DEFAULT_COLOR))
        return (('The username is not set.', DEFAULT_COLOR),)

    def redraw_window(self):
        self.setup_vars()
        self.draw_username_editing_window()
