from typing import TYPE_CHECKING, Any

from client.engine.event_handler import EventHandler
from client.engine.general_state.client_state import ClientState
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.general_state.queue_what import QueueWhat
from client.engine.graphics.graphics import Graphics
from client.engine.input.keyboard import KeyboardInput
from client.engine.input.mouse import MouseInput
from client.engine.primitives.event import InGameEvent
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput

from .events_processor import EventsProcessor

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


class ScreenManagerFactory:
    @staticmethod
    def create(
        *,
        initial_event: "Event",
        event_handler: Any,
    ) -> "ScreenManager":

        # Initialize the client state
        client_state = ClientState()
        client_state.initialize()

        # Initialize the profile
        profile_what = ProfileWhat()
        profile_what.set_profile("Default profile")

        # Initialize the queue
        queue_what = QueueWhat()
        queue_what.initialize(initial_event)

        return ScreenManager(
            KeyboardInput(),
            MouseInput(),
            Graphics(),
            event_handler,
        )


class ScreenManager:
    def __init__(
        self,
        keyboard_input: "KeyboardInput",
        mouse_input: "MouseInput",
        graphics: "Graphics",
        event_handler: Any,
    ):
        self.graphics = graphics
        self.keyboard_input = keyboard_input
        self.mouse_input = mouse_input
        self.events_processor = EventsProcessor(
            [event_handler, EventHandler()]  # Regular events and in game events
        )

    # Main loop
    def run(self) -> None:
        client_state = ClientState()
        queue_what = QueueWhat()
        # 1 - Push a sever polling event if needed
        ServerPolling.push_polling_event_if_needed()

        # 2 - Fetch and handle the latest event
        event = queue_what.queue.pop()

        # TODO: I don't like this if
        if event is not None and not isinstance(event, InGameEvent):
            self.events_processor.handle(event)

        # 3 - Read user input
        UserInput.process(self.keyboard_input, self.mouse_input)

        current_screen = client_state.get_current_screen()

        if current_screen is not None:
            # 4 - Draw the screen
            self.graphics.render(current_screen)

            # 5 - Update the current screen

            # TODO: I don't like this if
            if not isinstance(event, InGameEvent):
                event = None
            # it is an ingame event
            current_screen.update(event)
