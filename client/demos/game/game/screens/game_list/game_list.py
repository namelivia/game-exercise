# from client.engine.features.game_list.commands import GetGameList
# from client.engine.features.game_list.events import (
# ErrorGettingGameListEvent,
# UpdateGameListEvent,
# )
# from client.engine.features.game_management.commands import RequestJoiningAGame
# from client.engine.features.game_management.events import ErrorJoiningGameEvent

from engine.api import PlaySound, Screen, ScreenTransition, UserTypedEvent

from .ui import (
    create_background,
    create_cant_join_popup,
    create_error_popup,
    create_title,
)


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
        ]

        self.events = {
            UserTypedEvent: self.on_user_typed,
            # UpdateGameListEvent: self.on_game_list_updated,
            # ErrorGettingGameListEvent: self.on_error_getting_game_list,
            # ErrorJoiningGameEvent: self.on_error_joining_game,
        }

    def initialize(self):
        # GetGameList().execute()
        pass

    def on_user_typed(self, event: "UserTypedEvent") -> None:
        if event.key == "escape":
            PlaySound("assets/sounds/back.mp3").execute()
            from game.screens.lobby.lobby import Lobby

            ScreenTransition(Lobby).execute()
            return
        if event.key in "012345678":
            pass
        # RequestJoiningAGame(
        #     self.data["games"][int(event.key)].id,
        # ).execute()

    # def on_game_list_updated(self, event: "UpdateGameListEvent") -> None:
    # self.data["games"] = event.games

    # def on_error_getting_game_list(self, event: "ErrorGettingGameListEvent") -> None:
    # self.ui_elements[3].show()

    # def on_error_joining_game(self, event: "ErrorJoiningGameEvent") -> None:
    # self.ui_elements[4].show()
