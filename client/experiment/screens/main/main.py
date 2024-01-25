import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

from client.engine.features.sound.commands import PlaySound
from client.engine.features.user_input.events import UserClickedEvent
from client.engine.primitives.screen import Screen
from client.experiment.images import (
    BACKGROUND,
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
from client.experiment.sounds import CHEETAH, ELEPHANT, GIRAFFE, HYENA, LION, RHINO

from .ui import Background, Portrait

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState


class MainScreen(Screen):
    def __init__(self, client_state: "ClientState"):
        super().__init__(client_state)

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

        self.ui_elements = [
            Background(),
        ]

        for i, animal in enumerate(self.data["animals"]):
            self.ui_elements.append(
                Portrait(
                    animal["image"],
                    animal["highlight"],
                    50 + (i % 3) * 160,
                    50 + (i // 3) * 160,
                )
            )

        self.events = {UserClickedEvent: self.on_user_clicked}

    def on_user_clicked(self, event: UserClickedEvent) -> None:
        for i, element in enumerate(self.ui_elements):
            if isinstance(element, Portrait) and element.mouse_over:
                animal_name = self.data["animals"][i - 1]["name"]
                animal_sound = self.data["animals"][i - 1]["sound"]
                PlaySound(
                    self.client_state.profile, self.client_state.queue, animal_sound
                ).execute()
