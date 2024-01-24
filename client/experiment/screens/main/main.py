import logging
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

from client.engine.features.sound.commands import PlaySound
from client.engine.features.user_input.events import UserClickedEvent
from client.engine.primitives.screen import Screen

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
                    "image": "client/experiment/images/lion_black.png",
                    "highlight": "client/experiment/images/lion_color.png",
                    "sound": "client/experiment/sounds/lion.mp3",
                },
                {
                    "name": "Giraffe",
                    "image": "client/experiment/images/giraffe_black.png",
                    "highlight": "client/experiment/images/giraffe_color.png",
                    "sound": "client/experiment/sounds/giraffe.mp3",
                },
                {
                    "name": "Elephant",
                    "image": "client/experiment/images/elephant_black.png",
                    "highlight": "client/experiment/images/elephant_color.png",
                    "sound": "client/experiment/sounds/elephant.mp3",
                },
                {
                    "name": "Rhino",
                    "image": "client/experiment/images/rhino_black.png",
                    "highlight": "client/experiment/images/rhino_color.png",
                    "sound": "client/experiment/sounds/rhino.mp3",
                },
                {
                    "name": "Cheetah",
                    "image": "client/experiment/images/cheetah_black.png",
                    "highlight": "client/experiment/images/cheetah_color.png",
                    "sound": "client/experiment/sounds/cheetah.mp3",
                },
                {
                    "name": "Hyena",
                    "image": "client/experiment/images/hyena_black.png",
                    "highlight": "client/experiment/images/hyena_color.png",
                    "sound": "client/experiment/sounds/hyena.mp3",
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
                print(f"Clicked on {animal_name}")
                animal_sound = self.data["animals"][i - 1]["sound"]
                PlaySound(
                    self.client_state.profile, self.client_state.queue, animal_sound
                ).execute()
