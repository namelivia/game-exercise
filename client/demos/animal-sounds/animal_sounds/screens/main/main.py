import time

from animal_sounds.images import (
    CHEETAH_BLACK,
    CHEETAH_COLOR,
    ELEPHANT_BLACK,
    ELEPHANT_COLOR,
    GIRAFFE_BLACK,
    GIRAFFE_COLOR,
    HYENA_BLACK,
    HYENA_COLOR,
    LION_BLACK,
    LION_COLOR,
    RHINO_BLACK,
    RHINO_COLOR,
)
from animal_sounds.sounds import CHEETAH, ELEPHANT, GIRAFFE, HYENA, LION, RHINO
from engine.api import (
    ChangeCursor,
    ClickableUIElement,
    PlaySound,
    Screen,
    UserClickedEvent,
)

from .ui import create_background, create_portrait


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {
            "animals": [
                {
                    "name": "Lion",
                    "image": LION_BLACK,
                    "highlight": LION_COLOR,
                    "sound": LION,
                },
                {
                    "name": "Giraffe",
                    "image": GIRAFFE_BLACK,
                    "highlight": GIRAFFE_COLOR,
                    "sound": GIRAFFE,
                },
                {
                    "name": "Elephant",
                    "image": ELEPHANT_BLACK,
                    "highlight": ELEPHANT_COLOR,
                    "sound": ELEPHANT,
                },
                {
                    "name": "Rhino",
                    "image": RHINO_BLACK,
                    "highlight": RHINO_COLOR,
                    "sound": RHINO,
                },
                {
                    "name": "Cheetah",
                    "image": CHEETAH_BLACK,
                    "highlight": CHEETAH_COLOR,
                    "sound": CHEETAH,
                },
                {
                    "name": "Hyena",
                    "image": HYENA_BLACK,
                    "highlight": HYENA_COLOR,
                    "sound": HYENA,
                },
            ]
        }

        self.ui_elements = [create_background()]

        for i, animal in enumerate(self.data["animals"]):
            self.ui_elements.append(
                create_portrait(
                    animal["image"],
                    animal["highlight"],
                    95 + (i % 3) * 160,
                    97 + (i // 3) * 160,
                    lambda animal=animal: self.handle_animal_click(animal),
                )
            )

        self.events = {UserClickedEvent: self.on_user_clicked}

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        for element in self.ui_elements:
            if isinstance(element, ClickableUIElement) and element.mouse_over:
                element.clicked()

    def handle_animal_click(self, animal: dict) -> None:
        PlaySound(animal["sound"]).execute()
