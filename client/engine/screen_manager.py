from client.engine.event_handler import EventHandler
from client.game.event_handler import EventHandler as GameEventHandler
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput

from client.engine.primitives.event import InGameEvent
from .events_processor import EventsProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.input.input import Input
    from client.engine.graphics.graphics import Graphics


class ScreenManager:
    def __init__(
        self,
        client_state: "ClientState",
        input_manager: "Input",
        graphics: "Graphics",
    ):
        self.client_state = client_state
        self.graphics = graphics
        self.input_manager = input_manager
        self.event_processor = EventsProcessor(
            [EventHandler(), GameEventHandler()]  # Regular events and in game events
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
        UserInput.process(self.input_manager, self.client_state)

        current_screen = self.client_state.get_current_screen()

        if current_screen is not None:
            # 5 - Draw the screen
            self.graphics.render(current_screen)

            # 6 - Update the current screen

            # TODO: I don't like this if
            if event is not None and isinstance(event, InGameEvent):
                # it is an ingame event
                current_screen.update(event)
