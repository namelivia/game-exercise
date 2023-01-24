from client.engine.event_handler import EventHandler
from client.game.event_handler import EventHandler as GameEventHandler
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput

# from client.engine.primitives.event import InGameEvent
from .events_processor import EventsProcessor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.input_manager import InputManager
    from client.engine.graphics.graphics import Graphics


class ScreenManager:
    def __init__(
        self,
        client_state: "ClientState",
        input_manager: "InputManager",
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
        """
        # TODO: I don't like this if
        if not isinstance(event, InGameEvent):
            self.event_processor.handle(event, self.client_state)
        """
        self.event_processor.handle(event, self.client_state)

        # 4 - Draw the screen
        self.graphics.render(self.client_state.get_current_screen())

        # 5 - Read user input
        UserInput.process(self.input_manager, self.client_state)

        # 6 - Update the current screen
        """
        # TODO: I don't like this if
        in_game_event = None
        if isinstance(event, InGameEvent):
            in_game_event = event
        """
        in_game_event = event
        self.client_state.get_current_screen().update(in_game_event)
