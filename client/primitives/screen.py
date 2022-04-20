from abc import ABC


class Screen(ABC):
    def __init__(self, client_state):
        self.client_state = client_state
        self.ui_elements = []  # UI elements on the screen
        self.initial_time = client_state.clock.get()
        self.time = 0
        self.data = {}  # Internal state for the screen

    def get_ui_elements(self):
        return self.ui_elements

    def update(self):
        self.time = self.client_state.clock.get() - self.initial_time

        # Update ui elements they need to access the data and time to do so
        [element.update(self.time, self.data) for element in self.ui_elements]
