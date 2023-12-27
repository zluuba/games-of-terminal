from games_of_terminal.utils import draw_message


def show_placeholder_stub(height, width, window, color, message='In development.'):
    y = height // 2
    x = (width // 2) - (len(message) // 2)

    window.clear()
    draw_message(y, x, window, message, color)
