from abc import ABC
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from engine.clock import Clock
from engine.features.render.commands import RefreshRenderScreen
from engine.ui.clickable import ClickableUIElement
from engine.ui.ui import UIElement

if TYPE_CHECKING:
    from engine.primitives.event import InGameEvent
    from engine.primitives.timer import Timer


class JSONScreen(ABC):
    def __init__(self) -> None:
        self.ui_elements: List[UIElement | ClickableUIElement] = []
        self.timers: List["Timer"] = []  # Time based actions
        self.events: Dict[Any, Callable[[Any], None]] = (
            {}
        )  # Event based actions # TODO: Type this, should be InGameEvent > Callable
        self.initial_time = Clock().get_ticks()
        self.time = 0
        self.data: Dict[str, Any] = {}  # Internal state for the screen
        self.initial_actions = []

    def initialize(self) -> None:
        for action in self.initial_actions:
            action.execute()

    def update_events(self, event: Optional["InGameEvent"] = None) -> None:
        if event is not None:
            event_type = event.__class__
            if event_type in self.events:
                self.events[event_type](event)
        return None

    def add_timer(self, timer):
        self.timers.append(timer)

    def set_initial_actions(self, initial_actions):
        self.initial_actions = initial_actions

    def update(self) -> None:
        self.time = Clock().get_ticks() - self.initial_time
        for timer in self.timers:
            timer.update()

        # Cleanup inactive timers
        self.timers = [timer for timer in self.timers if timer.is_active()]
        for element in self.ui_elements:
            element.update(self.time, self.data)
        return None

    def add_ui_element(self, new_ui_element) -> None:
        self.ui_elements.append(new_ui_element)
        RefreshRenderScreen(self).execute()
