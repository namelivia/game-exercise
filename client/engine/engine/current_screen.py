from typing import TYPE_CHECKING, Any, Optional, Type

from engine.features.render.commands import StartRendering

if TYPE_CHECKING:
    from engine.primitives.screen import Screen


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
        # Tell the render thread to start rendering
        StartRendering(current_screen).execute()
        self.current_screen = current_screen
