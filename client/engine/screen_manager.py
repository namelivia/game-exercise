import threading
from queue import Empty, SimpleQueue
from typing import TYPE_CHECKING, Any

from client.engine.event_handler import EventHandler
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.general_state.options import Options
from client.engine.general_state.profile_manager import ProfileManager
from client.engine.general_state.queue import QueueManager
from client.engine.graphics.graphics import Graphics
from client.engine.input.keyboard import KeyboardInput
from client.engine.input.mouse import MouseInput
from client.engine.primitives.event import InGameEvent
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput

from .events_processor import EventsProcessor

if TYPE_CHECKING:
    from client.engine.primitives.event import Event


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class SoundWorker(threading.Thread):

    def __init__(self, name, my_queue):
        super().__init__()
        self.name = name
        self.my_queue = my_queue
        # Event used to signal the thread to stop gracefully
        self.stop_event = threading.Event()
        # Log that the worked has started?

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        while not self.stop_event.is_set():
            try:
                # Use a small timeout to allow checking the stop_event
                event_data = self.my_queue.get(timeout=0.1)
                # self._process_event(event_data)
                # self.my_queue.task_done() # Indicate that the task is finished
            except Empty:
                # Expected when the queue is empty after the timeout
                print("No events")
                continue
            except StopThread:
                # Internal exception to cleanly exit the loop
                break
            except Exception as e:
                print(f"Error {e}")
                break


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
        """
        sound_queue = SimpleQueue()

        sound_thread = SoundWorker(
            name="Sound",
            my_queue=sound_queue,
        )

        sound_thread.start()
        """

        """
        The safe termination code for threads is missing
            while thread_a.is_alive() or thread_b.is_alive():
                time.sleep(0.2)
    
            # The main thread joins the workers to ensure they terminate
            thread_a.join()
            thread_b.join()
        """

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
        # 1 - Push a sever polling event if needed
        ServerPolling.push_polling_event_if_needed()

        # 2 - Fetch and handle the latest event
        event = QueueManager().main_queue().pop()

        # TODO: I don't like this if
        if event is not None and not isinstance(event, InGameEvent):
            self.events_processor.handle(event)

        # 3 - Read user input
        UserInput.process(self.keyboard_input, self.mouse_input)

        current_screen = CurrentScreen().get_current_screen()

        if current_screen is not None:
            # 4 - Draw the screen
            self.graphics.render(current_screen)

            # 5 - Update the current screen

            # TODO: I don't like this if
            if not isinstance(event, InGameEvent):
                event = None
            # it is an ingame event
            current_screen.update(event)
