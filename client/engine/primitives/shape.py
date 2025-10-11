from abc import ABC
from typing import Any


class Shape(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hidden = False

    def load(self) -> None:
        pass

    def render(self, window: Any) -> None:
        pass

    def draw(self, window: Any) -> None:
        if not self.hidden:
            self.render(window)

    def hide(self) -> None:
        self.hidden = True

    def show(self) -> None:
        self.hidden = False

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def set_x(self, x: int) -> None:
        self.x = x

    def set_y(self, y: int) -> None:
        self.y = y

    # TODO: Transform these two into @abstractmethod
    def get_width(self) -> int:
        return 0

    def get_height(self) -> int:
        return 0
