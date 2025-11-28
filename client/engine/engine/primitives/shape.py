from abc import ABC
from typing import Any
from uuid import uuid4


class Shape(ABC):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hidden = False
        self.name = uuid4()

    def load(self) -> None:
        pass

    def render(self, x, y, opacity, window: Any, index) -> None:
        pass

    def draw(self, state, window: Any, index) -> None:
        if not self.hidden:
            # Add the local x and y to the coordinates
            self.render(
                state.get_x() + self.x,
                state.get_y() + self.y,
                state.get_opacity,
                window,
                index,
            )

    def hide(self) -> None:
        self.hidden = True

    def show(self) -> None:
        self.hidden = False

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_index(self):
        return 0

    def set_x(self, x: int) -> None:
        self.x = x

    def set_name(self, name: str) -> None:
        self.name = name

    def set_y(self, y: int) -> None:
        self.y = y

    # TODO: Transform these two into @abstractmethod
    def get_width(self) -> int:
        return 0

    def get_height(self) -> int:
        return 0
