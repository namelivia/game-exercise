from client.engine.features.user_input.commands import UserTyped
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.input.input import Input


class UserInput:
    @staticmethod
    def process(input_manager: "Input", client_state: "ClientState") -> None:
        # Get events from user input
        user_events = input_manager.read()

        # Run the user typed command for each user event
        for user_event in user_events:
            UserTyped(client_state.profile, client_state.queue, user_event).execute()
