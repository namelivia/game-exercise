import threading
import time

from client.engine.backend.foundational_wrapper import FoundationalWrapper
from client.engine.features.user_input.commands import UserClicked, UserTyped
from client.engine.features.user_input.keyboard import KeyboardInput
from client.engine.features.user_input.mouse import MouseInput


class StopThread(Exception):
    """Exception raised to signal a thread to stop processing."""

    pass


class UserInputWorker(threading.Thread):

    def __init__(self, name):
        super().__init__()
        self.name = name
        # Event used to signal the thread to stop gracefully
        self.stop_event = threading.Event()
        # Log that the worked has started?
        self.keyboard_input = KeyboardInput()
        self.mouse_input = MouseInput()

    def process(self) -> None:
        events = FoundationalWrapper.get_event()
        # Get events from keyboard
        keyboard_events = self.keyboard_input.read(events)

        # Run the user typed command for each user event
        for keyboard_event in keyboard_events:
            UserTyped(keyboard_event).execute()

        # Get events from mouse, currently only one event is returned
        mouse_event = self.mouse_input.read(events)

        # If there is a mouse event, run the user clicked command
        if mouse_event is not None:
            UserClicked().execute()

    def run(self):
        """The main execution loop for the thread."""
        print(f"[{self.name}] Thread started, waiting for events...")
        while not self.stop_event.is_set():
            try:
                self.process()
                time.sleep(0.01)
            except StopThread:
                # Internal exception to cleanly exit the loop
                break
            except Exception as e:
                print(f"Error {e}")
                break
