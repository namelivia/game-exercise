from typing import TYPE_CHECKING, Any, Dict, Type

from client.engine.commands import (
    GameCreatedInGameCommand,
    PlayerJoinedInGameCommand,
    PlayerWinsInGameCommand,
)
from client.engine.events import InitiateGameEvent
from client.engine.general_state.current_screen import CurrentScreen
from client.engine.general_state.profile_what import ProfileWhat
from client.engine.primitives.event_handler import EventHandler as BaseEventHandler
from common.events import GameCreated as GameCreatedInGameEvent  # TODO: akward
from common.events import PlayerJoined as PlayerJoinedInGameEvent  # TODO: akward
from common.events import PlayerWins as PlayerWinsInGameEvent  # TODO: akward

from .events import ClearInternalGameInformationEvent, ScreenTransitionEvent
from .screens.credits.credits import Credits
from .screens.enter_name.enter_name import EnterName
from .screens.game_list.game_list import GameList
from .screens.in_game.in_game import InGame
from .screens.intro.intro import Intro
from .screens.join_game.join_game import JoinGame
from .screens.lobby.lobby import Lobby
from .screens.new_game.new_game import NewGame
from .screens.options.options import Options
from .screens.profiles.profiles import Profiles

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedInGameEventHandler(BaseEventHandler[GameCreatedInGameEvent]):
    def handle(self, event: GameCreatedInGameEvent) -> None:
        GameCreatedInGameCommand(event.player_id).execute()


class PlayerJoinedInGameEventHandler(BaseEventHandler[PlayerJoinedInGameEvent]):
    def handle(self, event: PlayerJoinedInGameEvent) -> None:
        PlayerJoinedInGameCommand(event.player_id).execute()


class PlayerWinsInGameEventHandler(BaseEventHandler[PlayerWinsInGameEvent]):
    def handle(self, event: PlayerWinsInGameEvent) -> None:
        PlayerWinsInGameCommand(event.player_id).execute()


#################################################################


class InitiateGameEventHandler(BaseEventHandler[InitiateGameEvent]):
    def handle(self, event: InitiateGameEvent) -> None:
        # TODO: Why is it not an screen transition event??? Just because it contains more data?
        CurrentScreen().set_current_screen(
            InGame(
                event.game_data.events,
                event.game_data.id,
                event.game_data.name,
                event.game_data.players,
            )
        )


class ScreenTransitionEventHandler(BaseEventHandler[ScreenTransitionEvent]):
    def handle(self, event: ScreenTransitionEvent) -> None:
        current_screen = CurrentScreen()
        # Could I just push the instances to the queue?
        if event.dest_screen == "intro":
            current_screen.set_current_screen(Intro())
        if event.dest_screen == "lobby":
            current_screen.set_current_screen(Lobby())
        if event.dest_screen == "new_game_screen":
            current_screen.set_current_screen(NewGame())
        if event.dest_screen == "join_a_game":
            current_screen.set_current_screen(JoinGame())
        if event.dest_screen == "game_list":
            current_screen.set_current_screen(GameList())
        if event.dest_screen == "options":
            current_screen.set_current_screen(Options())
        if event.dest_screen == "credits":
            current_screen.set_current_screen(Credits())
        if event.dest_screen == "enter_name":
            current_screen.set_current_screen(EnterName())
        if event.dest_screen == "profiles":
            current_screen.set_current_screen(Profiles())


class ClearInternalGameInformationEventHandler(
    BaseEventHandler[ClearInternalGameInformationEvent]
):
    def handle(self, event: ClearInternalGameInformationEvent) -> None:
        profile_what = ProfileWhat()
        profile_what.profile.set_game(None)
        profile_what.profile.set_game_event_pointer(None)


handlers_map: Dict[Type["Event"], Any] = {
    ScreenTransitionEvent: ScreenTransitionEventHandler,
    ClearInternalGameInformationEvent: ClearInternalGameInformationEventHandler,
    InitiateGameEvent: InitiateGameEventHandler,
    # In game events, these events define the status of the game
    GameCreatedInGameEvent: GameCreatedInGameEventHandler,
    PlayerJoinedInGameEvent: PlayerJoinedInGameEventHandler,
    PlayerWinsInGameEvent: PlayerWinsInGameEventHandler,
}


class EventHandler(BaseEventHandler["Event"]):
    def handle(self, event: "Event") -> None:
        handlers_map[type(event)]().handle(event)
