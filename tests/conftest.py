import pytest


@pytest.fixture
def color_schemes():
    return [
        {'name': 'scheme1', 'selected': False},
        {'name': 'selected_scheme', 'selected': True},
        {'name': 'scheme2', 'selected': False},
    ]


@pytest.fixture
def selected_color_scheme_name():
    return 'selected_scheme'


@pytest.fixture
def settings_default_selected():
    return [
        {'name': 'option1', 'selected': False},
        {'name': 'option2', 'selected': True, 'default': True},
        {'name': 'option3', 'selected': False},
    ]


@pytest.fixture
def settings_default_unselected():
    return [
        {'name': 'option1', 'selected': False, 'default': True},
        {'name': 'option2', 'selected': True},
        {'name': 'option3', 'selected': False},
    ]
