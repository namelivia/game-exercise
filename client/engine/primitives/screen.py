from abc import ABC


class Screen(ABC):
    def __init__(self, client_state):
        self.client_state = client_state
        self.ui_elements = []  # UI elements on the screen
        self.timers = {}  # Time based actions
        self.events = {}  # Event based actions
        self.initial_time = client_state.clock.get()
        self.time = 0
        self.data = {}  # Internal state for the screen

    def get_ui_elements(self):
        return self.ui_elements

    def update(self, event=None):
        self.time = self.client_state.clock.get() - self.initial_time

        # TODO: These can be skipped sometimes, I have to fix this
        # Process timers
        if self.time in self.timers:
            self.timers[self.time]()

        # Process events
        if event is not None:
            event_type = event.__class__
            if event_type in self.events:
                self.events[event_type](event)

        # Update ui elements they need to access the data and time to do so
        [element.update(self.time, self.data) for element in self.ui_elements]
