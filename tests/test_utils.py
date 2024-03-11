from games_of_terminal.constants import MIN_WIN_HEIGHT, MIN_WIN_WIDTH
from games_of_terminal.utils import (
    too_small_window_handler, get_current_color_scheme_name,
    is_current_setting_option_is_default,
)

import pytest


def test_too_small_window_handler():
    with pytest.raises(SystemExit):
        too_small_window_handler(MIN_WIN_HEIGHT / 2, MIN_WIN_WIDTH / 2)

    too_small_window_handler(MIN_WIN_HEIGHT, MIN_WIN_WIDTH)
    too_small_window_handler(MIN_WIN_HEIGHT ** 2, MIN_WIN_WIDTH ** 2)


def test_get_current_color_scheme_name(color_schemes,
                                       selected_color_scheme_name):

    curr_selected_scheme_name = get_current_color_scheme_name(color_schemes)
    assert selected_color_scheme_name == curr_selected_scheme_name


def test_is_current_setting_option_is_default(settings_default_selected,
                                              settings_default_unselected):

    default_selected_res = is_current_setting_option_is_default(
        settings_default_selected
    )
    default_unselected_res = is_current_setting_option_is_default(
        settings_default_unselected
    )

    assert default_selected_res
    assert not default_unselected_res
