from abc import ABC


class UIElementState(ABC):
    def __init__(self, x, y, opacity=1):
        self.x = x
        self.y = y
        self.opacity = opacity

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_opacity(self, opacity):
        self.opacity = opacity

    def set_opacity(self, opacity):
        self.opacity = opacity
