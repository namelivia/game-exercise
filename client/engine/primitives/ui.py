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
