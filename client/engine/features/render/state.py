from typing import Any, Optional, Type


# This is a singleton
class State:
    _instance = None

    def __new__(cls: Type["State"], *args: Any, **kwargs: Any) -> "State":
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.is_rendering = False

    def get_is_rendering(self) -> bool:
        return self.is_rendering

    def start_rendering(self) -> None:
        self.is_rendering = True
