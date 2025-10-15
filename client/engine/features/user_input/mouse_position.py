from typing import Any, Tuple, Type

from client.engine.backend.input import InputBackend


class MousePosition:
    _instance = None

    # This class is a singleton
    def __new__(
        cls: Type["MousePosition"], *args: Any, **kwargs: Any
    ) -> "MousePosition":
        if not cls._instance:
            cls._instance = super(MousePosition, cls).__new__(cls)
        return cls._instance

    def get(self) -> Tuple[int, int]:
        return InputBackend.get_mouse_position()
