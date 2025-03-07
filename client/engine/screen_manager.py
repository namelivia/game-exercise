from typing import TYPE_CHECKING, Any

from client.engine.event_handler import EventHandler
from client.engine.general_state.client_state import ClientState
from client.engine.graphics.graphics import Graphics
from client.engine.input.keyboard import KeyboardInput
from client.engine.input.mouse import MouseInput
from client.engine.primitives.event import InGameEvent
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput

from .events_processor import EventsProcessor

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import Event


class ScreenManagerFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        event_handler: Any,
    ) -> "ScreenManager":
        client_state = ClientState()
        client_state.initialize()
        client_state.push_initial_event(initial_event)
        client_state.set_profile("Default profile")
        return ScreenManager(
            client_state,
            KeyboardInput(),
            MouseInput(),
            Graphics(),
            event_handler,
        )


class ScreenManager:
    def __init__(
        self,
        client_state: "ClientState",
        keyboard_input: "KeyboardInput",
        mouse_input: "MouseInput",
        graphics: "Graphics",
        event_handler: Any,
    ):
        self.client_state = client_state
        self.graphics = graphics
        self.keyboard_input = keyboard_input
        self.mouse_input = mouse_input
        self.event_processor = EventsProcessor(
            [event_handler, EventHandler()]  # Regular events and in game events
        )

    # Main loop
    def run(self) -> None:
        # 1 - Push a sever polling event if needed
        ServerPolling.push_polling_event_if_needed()

        # 2 - Fetch and handle the latest event
        event = self.client_state.queue.pop()

        # TODO: I don't like this if
        if event is not None and not isinstance(event, InGameEvent):
            self.event_processor.handle(event, self.client_state)

        # 3 - Read user input
        UserInput.process(self.keyboard_input, self.mouse_input)

        current_screen = self.client_state.get_current_screen()

        if current_screen is not None:
            # 4 - Draw the screen
            self.graphics.render(current_screen)

            # 5 - Update the current screen

            # TODO: I don't like this if
            if not isinstance(event, InGameEvent):
                event = None
            # it is an ingame event
            current_screen.update(event)
