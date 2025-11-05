from abc import ABC
from typing import Any, Dict

from engine.features.render.ui_element import UIElementRender

from .logic import UIElementLogic


# The UI Element has three parts, the logic part, the
# render part, and the shared state between the two, it currently only holds
# the coordinates.
class UIElement(ABC):
    def __init__(self, render, logic) -> None:
        self.render = render
        self.logic = logic

    def get_render(self) -> UIElementRender:
        return self.render

    def get_logic(self) -> UIElementLogic:
        return self.logic

    def show(self):
        self.render.show()

    def hide(self):
        self.render.hide()

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.logic.update(time, data)
