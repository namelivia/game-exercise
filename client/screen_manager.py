from client.commands import UserTyped
from client.event_handler import EventHandler
from client.game.event_handler import EventHandler as GameEventHandler
from client.commands import RequestGameStatus
from .events_processor import EventsProcessor


class ScreenManager:

    # Would I need all this? Maybe not, only someties if using pygame
    def __init__(self, client_state, input_manager, graphics):
        self.client_state = client_state  # Always
        self.graphics = graphics  # Only pygame
        self.input_manager = input_manager  # Only pygame

        self.event_processor = EventsProcessor([EventHandler(), GameEventHandler()])

    def _read_user_input(self):
        if self.input_manager is not None:
            user_events = self.input_manager.read()  # Get the user input
            for user_event in user_events:
                # Execute a command that will push the user input event to the queue
                UserTyped(
                    self.client_state.profile, self.client_state.queue, user_event
                ).execute()

    def push_polling_event(self):
        # Do the polling once every 1000 cycles
        polling_rate = 1000
        game_id = self.client_state.profile.game_id
        if self.client_state.clock.get() % polling_rate == 0 and game_id is not None:
            RequestGameStatus(
                self.client_state.profile, self.client_state.queue, game_id
            ).execute()

    def run(self):
        self.client_state.clock.tick()  # Update the clock
        self.push_polling_event()
        queued_event = self.client_state.queue.pop()  # Fetch the latest event

        self.event_processor.handle(  # Process the event
            queued_event, self.client_state
        )

        self.graphics.render(
            self.client_state.get_current_screen()
        )  # Render the screen

        self._read_user_input()

        # The screens may also use the event to update their internal state
        self.client_state.get_current_screen().update(queued_event)
