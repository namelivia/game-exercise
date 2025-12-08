from components.api import ImageCursor, create_fade_in
from engine.api import (
    ClickableUIElement,
    DisableUserInput,
    EnableUserInput,
    HideCursor,
    PlayMusic,
    PlaySound,
    Screen,
    Timer,
    UserClickedEvent,
)
from labyrinth.events import SetCustomCursorEvent
from labyrinth.ui_loader import load_ui


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        # Only for this screen
        self.ui_elements = load_ui("labyrinth/screens/main/ui.json")

        # Common for every screen
        self.custom_cursor = ImageCursor()
        self.custom_cursor.initialize(
            {
                "default": "assets/images/arrow_default.png",
                "go_left": "assets/images/arrow_left.png",
                "go_right": "assets/images/arrow_right.png",
                "go_forward": "assets/images/arrow_forward.png",
                "go_back": "assets/images/arrow_back.png",
                "look": "assets/images/look.png",
            }
        )
        self.custom_cursor.get_element().hide()
        self.ui_elements += [self.custom_cursor.get_element(), create_fade_in()]

        # Only for this screen
        self.timers = [Timer(700, self.on_intro_finished)]

    # Only for this screen
    def initialize(self):
        PlayMusic(
            "assets/sounds/ambient.ogg",
        ).execute()
        PlaySound(
            "assets/sounds/intro.ogg",
        ).execute()
        DisableUserInput().execute()
        HideCursor().execute()

        # Common for every screen
        self.events = {
            UserClickedEvent: self.on_user_clicked,
            SetCustomCursorEvent: self.on_set_custom_cursor,
        }

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        for element in self.ui_elements:
            if isinstance(element, ClickableUIElement) and element.mouse_over:
                element.clicked()

    # Only for this screen
    def on_intro_finished(self) -> None:
        EnableUserInput().execute()
        self.custom_cursor.set_cursor("default")

    # Common for every screen
    def on_set_custom_cursor(self, event: SetCustomCursorEvent) -> None:
        self.custom_cursor.set_cursor(event.key)
