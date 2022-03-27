from client.game.commands import UserTyped
from client.game.event_handler import EventHandler
from client.game.events import RefreshGameStatusEvent


class ScreenManager():

    # Would I need all this? Maybe not, only someties if using pygame
    def __init__(self, client_state, input_manager, graphics):
        self.client_state = client_state  # Always
        self.graphics = graphics  # Only pygame
        self.input_manager = input_manager  # Only pygame

        self.event_handler = EventHandler()

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

    def push_polling_event(self):
        # Do the polling once every 1000 cycles
        polling_rate = 1000
        game_id = self.client_state.profile.game_id
        if self.client_state.clock.get() % polling_rate == 0 and game_id is not None:
            self.client_state.queue.put(RefreshGameStatusEvent(game_id))

    def run(self):
        self.client_state.clock.tick()  # Update the clock
        self.push_polling_event()
        queued_event = self.client_state.queue.pop()  # Fetch the latest event

        self.event_handler.handle(  # Process the event
            queued_event,
            self.client_state,
            self.graphics
        )

        self.client_state.get_current_screen().render()  # Render the screen

        self._read_user_input()

        # The screens may also use the event to update their internal state
        self.client_state.get_current_screen().update(queued_event)
