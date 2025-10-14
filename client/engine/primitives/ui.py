from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

if TYPE_CHECKING:
    from client.engine.primitives.shape import Shape


class UIElement(ABC):
    def __init__(self) -> None:
        self.shapes: List["Shape"] = []

    # =============== STATE =========================
    # UI elements can hold a small state too that can be updated
    def update(self, time: int, data: Dict[str, Any]) -> None:
        pass

    def set_shapes(self, shapes: List["Shape"]) -> None:
        self.shapes = shapes

    # =============== RENDERING =========================
    def show(self) -> None:
        for shape in self.shapes:
            shape.show()

    def load(self) -> None:
        for shape in self.shapes:
            shape.load()
        return None

    def render(self, window: Any) -> None:
        for shape in self.shapes:
            shape.draw(window)
        return None


class ClickableUIElement:
    def __init__(self, on_click) -> None:
        self.element = UIElement()
        self.mouse_over = False
        self._was_mouse_over = False
        self.on_click = on_click

    # =============== STATE =========================
    def _is_mouse_over(self, x: int, y: int) -> bool:
        return (
            x > self.element.shapes[0].get_x()
            and x < self.element.shapes[0].get_x() + self.element.shapes[0].get_width()
            and y > self.element.shapes[0].get_y()
            and y < self.element.shapes[0].get_y() + self.element.shapes[0].get_height()
        )

    def on_mouse_enter(self) -> None:
        pass

    def on_mouse_leave(self) -> None:
        pass

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: Tuple[int, int]
    ) -> None:
        self.element.update(time, data)
        self._was_mouse_over = self.mouse_over
        self.mouse_over = self._is_mouse_over(mouse_position[0], mouse_position[1])
        if not self._was_mouse_over and self.mouse_over:
            self.on_mouse_enter()
        elif self._was_mouse_over and not self.mouse_over:
            self.on_mouse_leave()

    # ============= RENDER =========================
    def render(self, window: Any) -> None:
        self.element.render(window)

    def load(self) -> None:
        self.element.load()

    def show(self) -> None:
        self.element.show()

    def set_shapes(self, shapes: List["Shape"]) -> None:
        self.element.shapes = shapes
