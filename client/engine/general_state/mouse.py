from typing import Any, Tuple, Type

from client.engine.external.foundational_wrapper import FoundationalWrapper


# This is a singleton
class Mouse:
    _instance = None

    def __new__(cls: Type["Mouse"], *args: Any, **kwargs: Any) -> "Mouse":
        if not cls._instance:
            cls._instance = super(Mouse, cls).__new__(cls)
        return cls._instance

    def get(self) -> Tuple[int, int]:
        return FoundationalWrapper.get_mouse_position()
