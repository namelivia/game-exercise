from client.game.commands import UserTyped
from client.game.event_processor import EventProcessor


class ScreenManager():

    # Would I need all this? Maybe not, only someties if using pygame
    def __init__(self, client_state, input_manager, graphics):
        self.client_state = client_state  # Always
        self.graphics = graphics  # Only pygame
        self.input_manager = input_manager  # Only pygame

        self.event_processor = EventProcessor()

    def _read_user_input(self):
        if self.input_manager is not None:
            user_events = self.input_manager.read()  # Get the user input
            for user_event in user_events:
                # Execute a command that will push the user input event to the queue
                UserTyped(
                    self.client_state.profile,
                    self.client_state.queue,
                    user_event
                ).execute()

    def run(self):
        self.client_state.clock.tick()  # Update the clock
        queued_event = self.client_state.queue.pop()  # Fetch the latest event

        self.event_processor.process_event(  # Process the event
            queued_event,
            self.client_state,
            self.graphics
        )

        self.client_state.get_current_screen().render()  # Render the screen

        self._read_user_input()

        # The screens may also use the event to update their internal state
        self.client_state.get_current_screen().update(queued_event)
