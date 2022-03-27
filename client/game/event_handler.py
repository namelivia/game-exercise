from .events import (
    QuitGameEvent,
    ScreenTransitionEvent,
    NewGameRequestEvent,
    PlaceASymbolRequestEvent,
    JoinExistingGameEvent,
    InitiateGameEvent,
    RefreshGameStatusEvent,
    UpdateGameEvent
)
from .screens.intro.intro import Intro
from .screens.lobby.lobby import Lobby
from .screens.new_game.new_game import NewGame
from .screens.join_game.join_game import JoinGame
from .screens.in_game.in_game import InGame
from .commands import (
    CreateAGame,
    JoinAGame,
    PlaceASymbol,
    RefreshGameStatus
)


"""
Here we decide what to do with each of the events
"""


class EventHandler():
    def handle(self, event, client_state, graphics):
        if event is None:
            return
        print(event)
        # QUIT GAME
        if isinstance(event, QuitGameEvent):
            import pygame  # This is pygame dependent
            import sys
            pygame.quit()
            sys.exit()

        # TRANSITION TO OTHER SCREEN
        if isinstance(event, ScreenTransitionEvent):
            # Could I just push the instances to the queue?
            if event.dest_screen == "intro":
                client_state.set_current_screen(
                    Intro(client_state, graphics)
                )
            if event.dest_screen == "lobby":
                client_state.set_current_screen(
                    Lobby(client_state, graphics)
                )
            if event.dest_screen == "new_game_screen":
                client_state.set_current_screen(
                    NewGame(client_state, graphics)
                )
            if event.dest_screen == "join_a_game":
                client_state.set_current_screen(
                    JoinGame(client_state, graphics)
                )

        if isinstance(event, InitiateGameEvent):
            # TODO: Why is it not an screen transition event??? Just because it contains more data?
            client_state.set_current_screen(
                InGame(
                    client_state,
                    graphics,
                    event.turn,
                    event.board,
                    event.game_id,
                    event.name,
                    event.player_1_id,
                    event.player_2_id,
                )
            )

        if isinstance(event, UpdateGameEvent):
            # TODO: Why is it not an screen transition event??? Just because it contains more data?
            # TODO: Beware, uptating is actually re-creating the screen
            client_state.set_current_screen(
                InGame(
                    client_state,
                    graphics,
                    event.turn,
                    event.board,
                    event.game_id,
                    event.name,
                    event.player_1_id,
                    event.player_2_id,
                )
            )

        # TALK WITH THE SERVER
        if isinstance(event, NewGameRequestEvent):
            CreateAGame(
                client_state.profile,
                client_state.queue
            ).execute(event.new_game_name)

        if isinstance(event, PlaceASymbolRequestEvent):
            PlaceASymbol(
                client_state.profile,
                client_state.queue
            ).execute(event.position)

        if isinstance(event, JoinExistingGameEvent):
            JoinAGame(
                client_state.profile,
                client_state.queue
            ).execute(event.game_id)
        if isinstance(event, RefreshGameStatusEvent):
            RefreshGameStatus(
                client_state.profile,
                client_state.queue
            ).execute(event.game_id)
