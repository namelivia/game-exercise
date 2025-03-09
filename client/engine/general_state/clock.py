from typing import Any, Type

from client.engine.external.foundational_wrapper import FoundationalWrapper


class Clock:
    _instance = None

    # This class is a singleton
    def __new__(cls: Type["Clock"], *args: Any, **kwargs: Any) -> "Clock":
        if not cls._instance:
            cls._instance = super(Clock, cls).__new__(cls)
        return cls._instance

    def get(self) -> int:
        return FoundationalWrapper.get_clock_ticks()
