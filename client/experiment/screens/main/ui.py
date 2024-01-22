from typing import Any, Dict, List

from client.engine.graphics.shapes import Image
from client.engine.primitives.ui import ClickableUIElement, UIElement


class Background(UIElement):
    def __init__(self) -> None:
        super().__init__()
        self.shapes = [Image("client/experiment/images/background.png", 0, 0)]


class Lion(ClickableUIElement):
    def __init__(self) -> None:
        super().__init__()
        self.shapes = [
            Image("client/experiment/images/lion_black.png", 150, 150),
        ]

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: List[int]
    ) -> None:
        super().update(time, data, mouse_position)
        if self.mouse_over:
            self.shapes[0].hide()
        else:
            self.shapes[0].show()


class LionHighlight(UIElement):
    def __init__(self) -> None:
        self.shapes = [
            Image("client/experiment/images/lion_color.png", 150, 150),
        ]
