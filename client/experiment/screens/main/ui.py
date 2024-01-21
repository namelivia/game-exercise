from typing import Any, Dict

from client.engine.graphics.shapes import Animation, Image
from client.engine.primitives.ui import UIElement


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/experiment/images/background.png", 0, 0)]


class Coin(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Animation("client/experiment/images/coin", 0, 150),
        ]

    def update(self, time: int, data: Dict[str, Any]) -> None:
        animation_speed = 12  # The higher the slower
        if (time % animation_speed) == 0:
            animation_1 = self.shapes[0]
            if isinstance(animation_1, Animation):
                animation_1.update()  # Not supersure about this
        movement_speed = 5  # The higher the slower
        self.shapes[0].set_x(
            int((time / movement_speed) % 640)
        )  # Not supersure about this

    def _is_clicked(self, x: int, y: int) -> bool:
        return (
            x > self.shapes[0].get_x()
            and x < self.shapes[0].get_x() + self.shapes[0].get_width()
            and y > self.shapes[0].get_y()
            and y < self.shapes[0].get_y() + self.shapes[0].get_height()
        )

    def click(self, x: int, y: int) -> bool:
        if self._is_clicked(x, y):
            self.shapes[0].hide()
