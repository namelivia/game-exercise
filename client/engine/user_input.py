from typing import TYPE_CHECKING

from client.engine.external.foundational_wrapper import FoundationalWrapper
from client.engine.features.user_input.commands import UserClicked, UserTyped
from client.engine.features.user_input.keyboard import KeyboardInput
from client.engine.features.user_input.mouse import MouseInput

if TYPE_CHECKING:
    from client.engine.features.user_input.keyboard import KeyboardInput
    from client.engine.features.user_input.mouse import MouseInput


class UserInput:
    def __init__(self):
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
