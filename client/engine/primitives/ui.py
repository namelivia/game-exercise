from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

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

    def set_shapes(self, shapes: List["Shape"]) -> None:
        self.shapes = shapes

    def show(self) -> None:
        for shape in self.shapes:
            shape.show()


class ClickableUIElement:
    def __init__(self) -> None:
        self.element = UIElement()
        self.mouse_over = False

    def _is_mouse_over(self, x: int, y: int) -> bool:
        return (
            x > self.element.shapes[0].get_x()
            and x < self.element.shapes[0].get_x() + self.element.shapes[0].get_width()
            and y > self.element.shapes[0].get_y()
            and y < self.element.shapes[0].get_y() + self.element.shapes[0].get_height()
        )

    def render(self, window: Any) -> None:
        self.element.render(window)

    def show(self) -> None:
        self.element.show()

    def set_shapes(self, shapes: List["Shape"]) -> None:
        self.element.shapes = shapes

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: Tuple[int, int]
    ) -> None:
        self.element.update(time, data)
        self.mouse_over = self._is_mouse_over(mouse_position[0], mouse_position[1])
