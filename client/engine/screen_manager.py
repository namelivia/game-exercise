from client.engine.event_handler import EventHandler
from client.game.event_handler import EventHandler as GameEventHandler
from client.engine.server_polling import ServerPolling
from client.engine.user_input import UserInput
from .events_processor import EventsProcessor


class ScreenManager:
    def __init__(self, client_state, input_manager, graphics):
        self.client_state = client_state
        self.graphics = graphics
        self.input_manager = input_manager
        self.event_processor = EventsProcessor(
            [EventHandler(), GameEventHandler()]  # Regular events  # In game events
        )

    # Main loop
    def run(self):

        # 1 - Increase the clock
        self.client_state.clock.tick()

        # 2 - Push a sever polling event if needed
        ServerPolling.push_polling_event_if_needed(self.client_state)

        # 3 - Fetch and handle the latest event
        event = self.client_state.queue.pop()
        self.event_processor.handle(event, self.client_state)

        # 4 - Draw the screen
        self.graphics.render(self.client_state.get_current_screen())

        # 5 - Read user input
        UserInput.process(self.input_manager, self.client_state)

        # 6 - Update the current screen
        self.client_state.get_current_screen().update(event)
