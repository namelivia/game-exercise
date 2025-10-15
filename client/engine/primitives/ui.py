from abc import ABC
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

if TYPE_CHECKING:
    from client.engine.primitives.shape import Shape


# A UI Element can accept any custom logic
# right now custom logics are re-definitions of the update
# function
def create_ui_element(shapes: List["Shape"], custom_logic=None):
    if custom_logic is None:
        logic = UIElementLogic()
    else:
        logic = custom_logic
    return UIElement(UIElementRender(shapes), logic)


# This is the graphical representation of the UIElement
class UIElementRender(ABC):
    def __init__(self, shapes) -> None:
        self.shapes = shapes

    def show(self) -> None:
        for shape in self.shapes:
            shape.show()

    def hide(self) -> None:
        for shape in self.shapes:
            shape.hide()

    def load(self) -> None:
        for shape in self.shapes:
            shape.load()
        return None

    def render(self, window: Any) -> None:
        for shape in self.shapes:
            shape.draw(window)
        return None

    def contains_point(self, x, y):
        return (
            x > self.shapes[0].get_x()
            and x < self.shapes[0].get_x() + self.shapes[0].get_width()
            and y > self.shapes[0].get_y()
            and y < self.shapes[0].get_y() + self.shapes[0].get_height()
        )


# This is the logic part of the UIElement
# UI elements can hold a small state too that can be updated
# This is what will be extended.
class UIElementLogic(ABC):
    def update(self, time: int, data: Dict[str, Any]) -> None:
        pass


class UIElement(ABC):
    def __init__(self, render, logic) -> None:
        self.render = render
        self.logic = logic

    def get_render(self) -> UIElementRender:
        return self.render

    def get_logic(self) -> UIElementLogic:
        return self.logic


class ClickableUIElement:
    def __init__(
        self,
        element: "UIElement",
        on_click=None,
        on_mouse_enter=None,
        on_mouse_leave=None,
    ) -> None:
        self.element = element
        self.mouse_over = False
        self._was_mouse_over = False
        self.on_click = on_click
        self.on_mouse_enter = on_mouse_enter
        self.on_mouse_leave = on_mouse_leave

    def _is_mouse_over(self, x: int, y: int) -> bool:
        return self.element.get_render().contains_point(x, y)

    def clicked(self):
        if self.on_click is not None:
            self.on_click()

    def update(
        self, time: int, data: Dict[str, Any], mouse_position: Tuple[int, int]
    ) -> None:
        self.element.get_logic().update(time, data)
        self._was_mouse_over = self.mouse_over
        self.mouse_over = self._is_mouse_over(mouse_position[0], mouse_position[1])
        if not self._was_mouse_over and self.mouse_over:
            if self.on_mouse_enter is not None:
                self.on_mouse_enter()
        elif self._was_mouse_over and not self.mouse_over:
            if self.on_mouse_leave is not None:
                self.on_mouse_leave()

    def render(self, window: Any) -> None:
        self.element.get_render().render(window)

    def load(self) -> None:
        self.element.get_render().load()

    def show(self) -> None:
        self.element.get_render().show()

    def get_render(self) -> UIElementRender:
        return self.element.get_render()
