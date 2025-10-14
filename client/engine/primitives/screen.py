from abc import ABC
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from client.engine.general_state.clock import Clock
from client.engine.general_state.mouse import Mouse
from client.engine.primitives.ui import ClickableUIElement, UIElement

if TYPE_CHECKING:
    from client.engine.primitives.event import InGameEvent


class Screen(ABC):
    def __init__(self) -> None:
        self.ui_elements: List[UIElement | ClickableUIElement] = []
        self.timers: Dict[int, Callable[[], None]] = {}  # Time based actions
        self.events: Dict[Any, Callable[[Any], None]] = (
            {}
        )  # Event based actions # TODO: Type this, should be InGameEvent > Callable
        self.initial_time = Clock().get()
        self.time = 0
        self.data: Dict[str, Any] = {}  # Internal state for the screen

    # =============== STATE =========================
    def update(self, event: Optional["InGameEvent"] = None) -> None:
        self.time = Clock().get() - self.initial_time

        # TODO: These can be skipped sometimes, I have to fix this
        # Process timers
        if self.time in self.timers:
            self.timers[self.time]()

        # Process events
        if event is not None:
            event_type = event.__class__
            if event_type in self.events:
                self.events[event_type](event)

        # Update ui elements they need to access the data and time to do so
        # I'm also adding the mouse position for clickable elements.
        for element in self.ui_elements:
            if isinstance(element, ClickableUIElement):
                element.update(self.time, self.data, Mouse().get())
            else:
                element.update(self.time, self.data)
        return None

    # =============== RENDERING =========================
    def render(self, window) -> None:
        for ui_element in self.ui_elements:
            ui_element.render(window)

    def load(self) -> None:
        for ui_element in self.ui_elements:
            ui_element.load()
