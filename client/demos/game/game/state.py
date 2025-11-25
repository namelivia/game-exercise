from typing import Any, Type


class State:
    _instance = None

    def __new__(cls: Type["State"], *args: Any, **kwargs: Any) -> "State":
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.player_name = ""

    def set_player_name(self, name: str):
        self.player_name = name

    def get_player_name(self):
        return self.player_name
