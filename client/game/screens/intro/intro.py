from client.engine.features.sound.commands import PlayMusic, PlaySound
from client.engine.features.user_input.events import UserTypedEvent
from client.engine.primitives.screen import Screen
from client.engine.primitives.timer import Timer
from client.game.commands import ToLobby

from .ui import create_background, create_coin_1, create_coin_2, create_title


class Intro(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            create_title(),
            create_coin_1(),
            create_coin_2(),
        ]

        PlayMusic(
            "client/game/music/main_theme.mp3",
        ).execute()

        self.timers = [
            Timer(1000, self.show_coin_1),
            Timer(1200, self.show_coin_2),
            Timer(3000, self.go_back_to_lobby),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    # Actions
    def go_back_to_lobby(self) -> None:
        ToLobby().execute()

    def show_coin_1(self) -> None:
        PlaySound(
            "client/game/sounds/user_connected.mp3",
        ).execute()
        self.ui_elements[2].show()

    def show_coin_2(self) -> None:
        PlaySound(
            "client/game/sounds/user_connected.mp3",
        ).execute()
        self.ui_elements[3].show()

    def on_user_typed(self, event: UserTypedEvent) -> None:
        if event.key == "escape" or event.key == "return":
            PlaySound("client/game/sounds/select.mp3").execute()
            ToLobby().execute()
