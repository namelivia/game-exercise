from typing import TYPE_CHECKING, Any

from client.engine.event_handler import EventHandler
from client.engine.features.network.worker import NetworkWorker
from client.engine.features.render.worker import RenderWorker
from client.engine.features.sound.worker import SoundWorker
from client.engine.features.user_input.worker import UserInputWorker
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.general_state.options import Options
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.general_state.queue import QueueManager
from client.engine.primitives.event import InGameEvent
from client.engine.server_polling import ServerPolling

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
        ProfileManager().set_profile("Default profile")
        QueueManager().initialize(initial_event)
        CurrentScreen().initialize()
        Options().initialize()

        # Initialize render thread
        render_thread = RenderWorker(name="Render")

        render_thread.start()

        # Initialize sound thread
        sound_thread = SoundWorker(
            name="Sound",
            queue=QueueManager().get("sound"),
        )

        sound_thread.start()

        # Initialize user_input thread
        user_input_thread = UserInputWorker(name="UserInput")

        user_input_thread.start()

        # Initialize network thread
        network_thread = NetworkWorker(
            name="Network",
            queue=QueueManager().get("network"),
        )

        network_thread.start()

        return ScreenManager(
            event_handler,
        )


class ScreenManager:
    def __init__(
        self,
        event_handler: Any,
    ):
        self.events_processor = EventsProcessor(
            [event_handler, EventHandler()]  # Regular events and in game events
        )

    # Main loop
    def run(self) -> None:
        # 1 - Push a sever polling event if needed
        ServerPolling.push_polling_event_if_needed()

        # 2 - Fetch and handle the latest event
        event = QueueManager().main_queue().pop()

        # TODO: I don't like this if
        if event is not None and not isinstance(event, InGameEvent):
            self.events_processor.handle(event)

        current_screen = CurrentScreen().get_current_screen()

        if current_screen is not None:
            # 3 - Update the current screen

            # TODO: I don't like this if
            if not isinstance(event, InGameEvent):
                event = None
            # it is an ingame event
            current_screen.update(event)
