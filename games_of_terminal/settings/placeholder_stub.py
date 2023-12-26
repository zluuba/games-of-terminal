class PlaceholderStub:
    def __init__(self, height, width, window, color):
        self.height = height
        self.width = width
        self.window = window
        self.color = color
        self.stub_message = 'In development.'

    def show_stub(self):
        self.window.clear()

        y = self.height // 2
        x = (self.width // 2) - (len(self.stub_message) // 2)

        self.window.addstr(y, x, self.stub_message, self.color)
        self.window.refresh()
