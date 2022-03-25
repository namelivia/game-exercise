from .input_manager import InputManager
from .text_input_manager import TextInputManager


class Input():
    def __init__(self, uses_pygame):
        if (uses_pygame):
            self.manager = InputManager()
        else:
            self.manager = TextInputManager()

    def read(self):
        return self.manager.read()
