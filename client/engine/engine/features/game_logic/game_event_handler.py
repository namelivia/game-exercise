from typing import Any, Type


class GameEventHandler:
    _instance = None

    # This class is a singleton
    def __new__(
        cls: Type["GameEventHandler"], *args: Any, **kwargs: Any
    ) -> "GameEventHandler":
        if not cls._instance:
            cls._instance = super(GameEventHandler, cls).__new__(cls)
        return cls._instance

    def set(self, event_handler):
        self.event_handler = event_handler

    def get(self):
        return self.event_handler
