from typing import TYPE_CHECKING

from client.engine.features.user_input.commands import UserTyped

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.input.keyboard import KeyboardInput


class UserInput:
    @staticmethod
    def process(keyboard_input: "KeyboardInput", client_state: "ClientState") -> None:
        # Get events from keyboard
        keyboard_events = keyboard_input.read()

        # Run the user typed command for each user event
        for keyboard_event in keyboard_events:
            UserTyped(
                client_state.profile, client_state.queue, keyboard_event
            ).execute()
