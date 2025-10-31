from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from .screen import ScreenRender


class State:
    _instance = None

    def __new__(cls: Type["State"], *args: Any, **kwargs: Any) -> "State":
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.current_screen: Optional["ScreenRender"] = None

    def set_current_screen(self, screen: "ScreenRender") -> None:
        self.current_screen = screen

    def get_current_screen(self):
        return self.current_screen
