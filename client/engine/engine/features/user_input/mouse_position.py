from typing import Any, Tuple, Type

from .backend.pygame.input import InputBackend
from .state import State


class MousePosition:
    _instance = None

    def __new__(
        cls: Type["MousePosition"], *args: Any, **kwargs: Any
    ) -> "MousePosition":
        if not cls._instance:
            cls._instance = super(MousePosition, cls).__new__(cls)
        return cls._instance

    def get(self) -> Tuple[int, int]:
        # If the user input is disabled the mouse is "frozen"
        # in place
        state = State()
        if state.user_input_is_enabled():
            position = InputBackend.get_mouse_position()
            self.last_position = position
            return position
        return self.last_position
