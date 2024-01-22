from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from client.engine.primitives.shape import Shape


class UIElement(ABC):
    def __init__(self) -> None:
        self.shapes: List["Shape"] = []

    # TODO: Can I type pygame types?
    # UI elements can hold a small state too that can be updated
    def render(self, window: Any) -> None:
        for shape in self.shapes:
            shape.draw(window)
        return None

    def update(self, time: int, data: Dict[str, Any]) -> None:
        pass

    def show(self) -> None:
        for shape in self.shapes:
            shape.show()


class ClickableUIElement(UIElement):
    def __init__(self) -> None:
        super().__init__()
        self.mouse_over = False

    def _is_mouse_over(self, x: int, y: int) -> bool:
        return (
            x > self.shapes[0].get_x()
            and x < self.shapes[0].get_x() + self.shapes[0].get_width()
            and y > self.shapes[0].get_y()
            and y < self.shapes[0].get_y() + self.shapes[0].get_height()
        )

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: List[int]
    ) -> None:
        super().update(time, data)
