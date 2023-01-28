from typing import Any
from abc import ABC


class Shape(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hidden = False

    def hide(self) -> None:
        self.hidden = True

    def show(self) -> None:
        self.hidden = False

    def set_x(self, x: int) -> None:
        self.x = x

    def set_y(self, y: int) -> None:
        self.y = y

    # TODO: Can I type pygame types?
    def render(self, window: Any) -> None:
        pass

    # TODO: Can I type pygame types?
    def draw(self, window: Any) -> None:
        if not self.hidden:
            self.render(window)
