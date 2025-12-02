from components.api import create_fade_in, create_fade_out
from engine.api import (
    AnimationFinishedEvent,
    DisableUserInput,
    EnableUserInput,
    PlaySound,
    Screen,
    ScreenTransition,
    UserTypedEvent,
)

from .ui import (
    create_background,
    create_cant_join_popup,
    create_error_popup,
    create_title,
)

# from client.engine.features.game_list.commands import GetGameList
# from client.engine.features.game_list.events import (
# ErrorGettingGameListEvent,
# UpdateGameListEvent,
# )
# from client.engine.features.game_management.commands import RequestJoiningAGame
# from client.engine.features.game_management.events import ErrorJoiningGameEvent


class GameList(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.data = {"games": []}

        self.ui_elements = [
            create_background(),
            # create_game_list(self.data["games"]),
            create_title(),
            create_error_popup(),
            create_cant_join_popup(),
            create_fade_in(),
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            AnimationFinishedEvent: self.on_animation_finished,
            # UpdateGameListEvent: self.on_game_list_updated,
            # ErrorGettingGameListEvent: self.on_error_getting_game_list,
            # ErrorJoiningGameEvent: self.on_error_joining_game,
        }

    def initialize(self):
        DisableUserInput().execute()
        # GetGameList().execute()

    def on_user_typed(self, event: "UserTypedEvent") -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            self.add_ui_element(create_fade_out())
            DisableUserInput().execute()
            return
        if event.key in "012345678":
            pass
        # RequestJoiningAGame(
        #     self.data["games"][int(event.key)].id,
        # ).execute()

    def on_animation_finished(self, event: AnimationFinishedEvent) -> None:
        if event.key == "fade_in":
            EnableUserInput().execute()
        if event.key == "fade_out":
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            EnableUserInput().execute()

    # def on_game_list_updated(self, event: "UpdateGameListEvent") -> None:
    # self.data["games"] = event.games

    # def on_error_getting_game_list(self, event: "ErrorGettingGameListEvent") -> None:
    # self.ui_elements[3].show()

    # def on_error_joining_game(self, event: "ErrorJoiningGameEvent") -> None:
    # self.ui_elements[4].show()
