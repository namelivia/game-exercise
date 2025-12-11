from components.api import ImageCursor
from engine.api import ClickableUIElement, Screen, UserClickedEvent
from labyrinth.events import SetCustomCursorEvent
from labyrinth.ui_loader import load_ui


class AnotherScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {}
        self.ui_elements = load_ui("labyrinth/screens/another/ui.json")

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
        self.custom_cursor.set_cursor("default")
        self.ui_elements += [self.custom_cursor.get_element()]

        self.events = {
            UserClickedEvent: self.on_user_clicked,
            SetCustomCursorEvent: self.on_set_custom_cursor,
        }

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        for element in self.ui_elements:
            if isinstance(element, ClickableUIElement) and element.mouse_over:
                element.clicked()

    def on_set_custom_cursor(self, event: SetCustomCursorEvent) -> None:
        self.custom_cursor.set_cursor(event.key)
