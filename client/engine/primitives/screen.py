from abc import ABC
from typing import TYPE_CHECKING, List, Optional, Callable, Dict, Any

if TYPE_CHECKING:
    from client.engine.primitives.event import InGameEvent
    from client.engine.primitives.ui import UIElement
    from client.engine.general_state.client_state import ClientState


class Screen(ABC):
    def __init__(self, client_state: "ClientState"):
        self.client_state = client_state
        self.ui_elements: List[UIElement] = []  # UI elements on the screen
        self.timers: Dict[int, Callable[[], None]] = {}  # Time based actions
        self.events: Dict[
            Any, Callable[[Any], None]
        ] = (
            {}
        )  # Event based actions # TODO: Type this, should be InGameEvent > Callable
        self.initial_time = client_state.clock.get()
        self.time = 0
        self.data: Dict[str, Any] = {}  # Internal state for the screen

    def get_ui_elements(self) -> List["UIElement"]:
        return self.ui_elements

    def update(self, event: Optional["InGameEvent"] = None) -> None:
        self.time = self.client_state.clock.get() - self.initial_time

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
        for element in self.ui_elements:
            element.update(self.time, self.data)
        return None
