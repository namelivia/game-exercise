from client.engine.features.user_input.events import UserTypedEvent
from client.engine.primitives.screen import Screen

from .ui import OptionList, WelcomeMessage, create_background


class Lobby(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            # WelcomeMessage(self.data["name"], self.data["id"]),
            # OptionList(
            #    {
            #        "1": "Create a new game",
            #        "2": "Join an existing game",
            #        "3": "Game list",
            #        "4": "Options",
            #        "5": "Set Name",
            #        "6": "Credits",
            #        "7": "Profiles",
            #    }
            # ),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        pass
