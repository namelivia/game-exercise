from typing import TYPE_CHECKING, Any

from client.engine.event_handler import EventHandler
from client.engine.primitives.event import InGameEvent
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput

from .events_processor import EventsProcessor

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.graphics.graphics import Graphics
    from client.engine.input.keboard import KeboardInput


class ScreenManager:
    def __init__(
        self,
        client_state: "ClientState",
        keyboard_input: "KeboardInput",
        graphics: "Graphics",
        event_handler: Any,
    ):
        self.client_state = client_state
        self.graphics = graphics
        self.keyboard_input = keyboard_input
        self.event_processor = EventsProcessor(
            [event_handler, EventHandler()]  # Regular events and in game events
        )

    # Main loop
    def run(self) -> None:
        # 1 - Increase the clock
        self.client_state.clock.tick()

        # 2 - Push a sever polling event if needed
        ServerPolling.push_polling_event_if_needed(self.client_state)

        # 3 - Fetch and handle the latest event
        event = self.client_state.queue.pop()

        # TODO: I don't like this if
        if event is not None and not isinstance(event, InGameEvent):
            self.event_processor.handle(event, self.client_state)

        # 4 - Read user input
        UserInput.process(self.keyboard_input, self.client_state)

        current_screen = self.client_state.get_current_screen()

        if current_screen is not None:
            # 5 - Draw the screen
            self.graphics.render(current_screen)

            # 6 - Update the current screen

            # TODO: I don't like this if
            if not isinstance(event, InGameEvent):
                event = None
            # it is an ingame event
            current_screen.update(event)
