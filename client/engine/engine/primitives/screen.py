from abc import ABC
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from engine.clock import Clock
from engine.primitives.ui import ClickableUIElement, UIElement

if TYPE_CHECKING:
    from engine.primitives.event import InGameEvent
    from engine.primitives.timer import Timer


# This is the graphical representation of the screen
class Screen(ABC):
    def __init__(self) -> None:
        self.ui_elements: List[UIElement | ClickableUIElement] = []
        self.timers: List["Timer"] = []  # Time based actions
        self.events: Dict[Any, Callable[[Any], None]] = (
            {}
        )  # Event based actions # TODO: Type this, should be InGameEvent > Callable
        self.initial_time = Clock().get_ticks()
        self.time = 0
        self.data: Dict[str, Any] = {}  # Internal state for the screen

    def update_events(self, event: Optional["InGameEvent"] = None) -> None:
        if event is not None:
            event_type = event.__class__
            if event_type in self.events:
                self.events[event_type](event)
        return None

    def update(self) -> None:
        self.time = Clock().get_ticks() - self.initial_time
        for timer in self.timers:
            timer.update()
        for element in self.ui_elements:
            element.update(self.time, self.data)
        return None
