def show_placeholder_stub(height, width, window, color, message='In development.'):
    window.clear()

    y = height // 2
    x = (width // 2) - (len(message) // 2)

    window.addstr(y, x, message, color)
    window.refresh()
