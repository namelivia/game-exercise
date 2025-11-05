from typing import TYPE_CHECKING, Any, Dict

from engine.features.render.ui_element import UIElementRender
from engine.features.user_input.mouse_position import MousePosition

from .logic import UIElementLogic

if TYPE_CHECKING:
    from .ui import UIElement


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

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.element.update(time, data)
        self._was_mouse_over = self.mouse_over
        mouse_position = MousePosition().get()
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
        self.element.show()

    def get_render(self) -> UIElementRender:
        return self.element.get_render()

    def get_logic(self) -> UIElementLogic:
        return self.element.get_logic()
