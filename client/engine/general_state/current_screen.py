import uuid
from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from client.engine.primitives.screen import Screen


# This is a singleton
class CurrentScreen:
    _instance = None

    def __new__(
        cls: Type["CurrentScreen"], *args: Any, **kwargs: Any
    ) -> "CurrentScreen":
        if not cls._instance:
            cls._instance = super(CurrentScreen, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.current_screen: Optional["Screen"] = None

    def get_current_screen(self) -> Optional["Screen"]:
        return self.current_screen

    def set_current_screen(self, current_screen: "Screen") -> None:
        self.current_screen = current_screen
