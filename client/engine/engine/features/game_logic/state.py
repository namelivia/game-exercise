from typing import Any, Optional, Type

from engine.features.render.commands import StartRendering
from engine.primitives.screen import Screen


class State:
    _instance = None

    def __new__(cls: Type["State"], *args: Any, **kwargs: Any) -> "State":
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.current_screen: Optional["Screen"] = None

    def get_current_screen(self) -> Optional["Screen"]:
        return self.current_screen

    def set_current_screen(self, current_screen: "Screen") -> None:
        # Tell the render thread to start rendering
        StartRendering(current_screen).execute()
        self.current_screen = current_screen
