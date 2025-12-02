from abc import ABC
from typing import Any, Dict

from engine.clock import Clock


# This is the logic part of the UIElement
# UI elements can hold a small state too that can be updated
# This is what will be extended.
class UIElementLogic(ABC):
    def __init__(self, state, render):
        self.state = state
        self.render = render
        self.enabled = True
        self.initial_time = Clock().get_ticks()

    def update(self, time: int, data: Dict[str, Any]) -> None:
        self.relative_time = Clock().get_ticks() - self.initial_time
