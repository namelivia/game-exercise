from abc import ABC


class Shape(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hidden = False

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def render(self, window):
        pass

    def draw(self, window):
        if not self.hidden:
            self.render(window)
