from typing import Any, Type


class State:
    _instance = None

    def __new__(cls: Type["State"], *args: Any, **kwargs: Any) -> "State":
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.sound_on: bool = True

    def set_sound_on(self) -> None:
        self.sound_on = True

    def set_sound_off(self) -> None:
        self.sound_on = False

    def is_sound_on(self) -> bool:
        return self.sound_on
