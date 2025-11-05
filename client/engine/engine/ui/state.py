from abc import ABC


class UIElementState(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_index(self):
        return 0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y
