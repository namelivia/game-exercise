from typing import TYPE_CHECKING

from client.engine.features.user_input.commands import UserClicked, UserTyped
from client.engine.foundational_wrapper import FoundationalWrapper

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.input.keyboard import KeyboardInput
    from client.engine.input.mouse import MouseInput


class UserInput:
    @staticmethod
    def process(
        keyboard_input: "KeyboardInput",
        mouse_input: "MouseInput",
        client_state: "ClientState",
    ) -> None:
        events = FoundationalWrapper.get_event()
        # Get events from keyboard
        keyboard_events = keyboard_input.read(events)

        # Run the user typed command for each user event
        for keyboard_event in keyboard_events:
            UserTyped(
                client_state.profile, client_state.queue, keyboard_event
            ).execute()

        # Get events from mouse, currently only one event is returned
        mouse_event = mouse_input.read(events)

        # If there is a mouse event, run the user clicked command
        if mouse_event is not None:
            UserClicked(client_state.profile, client_state.queue).execute()
