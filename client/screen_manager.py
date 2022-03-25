from .game_specific.events import ScreenTransitionEvent

# This should manage transitions between states


class ScreenManager():

    # This will go somewhere else
    # Would I need all this? Maybe not, only someties if using pygame
    def __init__(self, client_state, input_manager, graphics):
        self.client_state = client_state  # Always
        self.graphics = graphics  # Only pygame
        self.input_manager = input_manager  # Only pygame

    def _process_queue_event(self, event):

        # The event is a screen transition one, these will override current_screen
        if type(event) is ScreenTransitionEvent:
            self.current_screen = event.execute(self.client_state, self.graphics)  # This is weird (passing the graphics)

    def run(self):
        # THIS IS THE MAIN CYCLE!!!!

        # CLOCK
        self.client_state.clock.tick()  # Update the clock

        # QUEUE
        # TODO: Am I ready to pickup the next event from the queue? Maybe not! But for now OK.
        queued_event = self.client_state.queue.pop()  # Get the event from the queue
        self._process_queue_event(queued_event)  # Process the queued event

        self.current_screen.render()  # Display (This is going to be generic, not pygame only)

        if self.input_manager is not None:
            user_events = self.input_manager.read()  # Get the user input (pygame only)

        # Execute commands using all together (this may add new events to the queue)
        # And apply it on the screen (may add new events to the queue?)
        self.current_screen.update(user_events)
