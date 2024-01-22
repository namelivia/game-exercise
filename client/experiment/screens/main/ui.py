from typing import Any, Dict, List

from client.engine.graphics.shapes import Animation, Image
from client.engine.primitives.ui import ClickableUIElement, UIElement


class Background(UIElement):
    def __init__(self) -> None:
        self.shapes = [Image("client/experiment/images/background.png", 0, 0)]


class Coin(ClickableUIElement):
    def __init__(self) -> None:
        self.shapes = [
            Animation("client/experiment/images/coin", 0, 150),
        ]

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: List[int]
    ) -> None:
        animation_speed = 12  # The higher the slower
        if (time % animation_speed) == 0:
            animation_1 = self.shapes[0]
            if isinstance(animation_1, Animation):
                animation_1.update()  # Not supersure about this
        movement_speed = 5  # The higher the slower
        self.shapes[0].set_x(
            int((time / movement_speed) % 640)
        )  # Not supersure about this
        self.mouse_over = self._is_mouse_over(mouse_position[0], mouse_position[1])
        if self.mouse_over:
            self.shapes[0].hide()
        else:
            self.shapes[0].show()
