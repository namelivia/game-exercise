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
    DisableUserInput,
    EnableUserInput,
    PlaySound,
    Screen,
    Timer,
    UserClickedEvent,
)

from .ui import create_background, create_overlay, create_portrait


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
                    "sound_length": 917,
                },
                {
                    "name": "Giraffe",
                    "image": GIRAFFE_BLACK,
                    "highlight": GIRAFFE_COLOR,
                    "sound": GIRAFFE,
                    "sound_length": 444,
                },
                {
                    "name": "Elephant",
                    "image": ELEPHANT_BLACK,
                    "highlight": ELEPHANT_COLOR,
                    "sound": ELEPHANT,
                    "sound_length": 950,
                },
                {
                    "name": "Rhino",
                    "image": RHINO_BLACK,
                    "highlight": RHINO_COLOR,
                    "sound": RHINO,
                    "sound_length": 2262,
                },
                {
                    "name": "Cheetah",
                    "image": CHEETAH_BLACK,
                    "highlight": CHEETAH_COLOR,
                    "sound": CHEETAH,
                    "sound_length": 855,
                },
                {
                    "name": "Hyena",
                    "image": HYENA_BLACK,
                    "highlight": HYENA_COLOR,
                    "sound": HYENA,
                    "sound_length": 1096,
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

        self.ui_elements.append(create_overlay())

        self.events = {UserClickedEvent: self.on_user_clicked}

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        for element in self.ui_elements:
            if isinstance(element, ClickableUIElement) and element.mouse_over:
                element.clicked()

    def reenable_user_input(self):
        ChangeCursor("ARROW").execute()
        EnableUserInput().execute()

    def handle_animal_click(self, animal: dict) -> None:
        ChangeCursor("WAIT").execute()
        PlaySound(animal["sound"]).execute()
        DisableUserInput().execute()
        self.add_timer(Timer(animal["sound_length"], self.reenable_user_input))

    def hide_overlay(self) -> None:
        self.ui_elements[-1].hide()
