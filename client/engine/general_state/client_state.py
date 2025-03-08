import uuid
from typing import TYPE_CHECKING, Any, Optional, Type

from .clock import Clock
from .mouse import Mouse

if TYPE_CHECKING:
    from client.engine.primitives.event import Event
    from client.engine.primitives.screen import Screen


# This is a singleton
class ClientState:
    _instance = None

    def __new__(cls: Type["ClientState"], *args: Any, **kwargs: Any) -> "ClientState":
        if not cls._instance:
            cls._instance = super(ClientState, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self.clock = Clock()
        self.mouse = Mouse()
        self.current_screen: Optional["Screen"] = None

    def get_current_screen(self) -> Optional["Screen"]:
        return self.current_screen

    def set_current_screen(self, current_screen: "Screen") -> None:
        self.current_screen = current_screen
