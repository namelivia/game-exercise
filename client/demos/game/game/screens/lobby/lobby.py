from components.api import create_fade_in
from engine.api import PlaySound, Screen, ScreenTransition, UserTypedEvent

from game.state import State

from .ui import create_background, create_options, create_welcome_message


class Lobby(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.ui_elements = [
            create_background(),
            create_welcome_message(),
            create_options(
                {
                    "1": "Create a new game",
                    "2": "Join an existing game",
                    "3": "Game list",
                    "4": "Options",
                    "5": "Set Name",
                    "6": "Credits",
                    "7": "Profiles",
                }
            ),
            create_fade_in(),
        ]

        self.events = {UserTypedEvent: self.on_user_typed}

    def initialize(self) -> None:
        self.data = {"player_name": State().get_player_name()}

    def on_user_typed(self, event: UserTypedEvent) -> None:
        key = event.key
        if key == "1":
            PlaySound("assets/sounds/select.mp3").execute()
            from game.screens.create_game.create_game import CreateGame

            ScreenTransition(CreateGame).execute()
            return
        if key == "2":
            PlaySound("assets/sounds/select.mp3").execute()
            from game.screens.join_game.join_game import JoinGame

            ScreenTransition(JoinGame).execute()
            return
        if key == "3":
            PlaySound("assets/sounds/select.mp3").execute()
            from game.screens.game_list.game_list import GameList

            ScreenTransition(GameList).execute()
            return
        if key == "4":
            PlaySound("assets/sounds/select.mp3").execute()
            from game.screens.options.options import Options

            ScreenTransition(Options).execute()
            return
        if key == "5":
            PlaySound("assets/sounds/select.mp3").execute()
            from game.screens.enter_name.enter_name import EnterName

            ScreenTransition(EnterName).execute()
            return
        if key == "6":
            PlaySound("assets/sounds/select.mp3").execute()
            from game.screens.credits.credits import Credits

            ScreenTransition(Credits).execute()
            return
        if key == "7":
            pass
