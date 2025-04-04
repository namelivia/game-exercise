from typing import Any, Dict, Tuple

from client.engine.graphics.shapes import Image
from client.engine.primitives.ui import ClickableUIElement, UIElement
from client.experiment.images import BACKGROUND


class Background(UIElement):
    def __init__(self) -> None:
        super().__init__()
        self.set_shapes([Image(BACKGROUND, 0, 0)])


class Portrait(ClickableUIElement):
    def __init__(self, image: str, highlight: str, x: int, y: int) -> None:
        super().__init__()
        self.image = Image(image, x, y)
        self.highlight = Image(highlight, x, y)
        self.set_shapes([self.image])

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: Tuple[int, int]
    ) -> None:
        super().update(time, data, mouse_position)
        if self.mouse_over:
            self.set_shapes([self.highlight])
        else:
            self.set_shapes([self.image])
