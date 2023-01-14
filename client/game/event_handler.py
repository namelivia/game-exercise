from client.engine.primitives.event_handler import EventHandler as BaseEventHandler
from client.engine.events import InitiateGameEvent
from .events import (
    ScreenTransitionEvent,
    ClearInternalGameInformationEvent,
)
from .screens.intro.intro import Intro
from .screens.lobby.lobby import Lobby
from .screens.new_game.new_game import NewGame
from .screens.join_game.join_game import JoinGame
from .screens.game_list.game_list import GameList
from .screens.options.options import Options
from .screens.in_game.in_game import InGame
from .screens.credits.credits import Credits
from .screens.enter_name.enter_name import EnterName
from .screens.profiles.profiles import Profiles
from client.engine.commands import (
    GameCreatedInGameCommand,
    PlayerJoinedInGameCommand,
    PlayerWinsInGameCommand,
)
from common.events import (
    GameCreated as GameCreatedInGameEvent,  # TODO: akward
    PlayerJoined as PlayerJoinedInGameEvent,  # TODO: akward
    PlayerWins as PlayerWinsInGameEvent,  # TODO: akward
)

"""
Currently event handlers are the one that do the processing.
They do the actual procssing and can execute commands.
"""


# ===== SERVER INGAME EVENTS COMMUNICATIONS ===== THIS ARE THE IN-GAME EVENTS PLACED BY THE SERVER
class GameCreatedInGameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        GameCreatedInGameCommand(
            client_state.profile, client_state.queue, event.player_id
        ).execute()


class PlayerJoinedInGameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        PlayerJoinedInGameCommand(
            client_state.profile, client_state.queue, event.player_id
        ).execute()


class PlayerWinsInGameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        PlayerWinsInGameCommand(
            client_state.profile, client_state.queue, event.player_id
        ).execute()


#################################################################


class InitiateGameEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        # TODO: Why is it not an screen transition event??? Just because it contains more data?
        client_state.set_current_screen(
            InGame(
                client_state,
                event.game_data.events,
                event.game_data.id,
                event.game_data.name,
                event.game_data.players,
            )
        )


class ScreenTransitionEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        # Could I just push the instances to the queue?
        if event.dest_screen == "intro":
            client_state.set_current_screen(Intro(client_state))
        if event.dest_screen == "lobby":
            client_state.set_current_screen(Lobby(client_state))
        if event.dest_screen == "new_game_screen":
            client_state.set_current_screen(NewGame(client_state))
        if event.dest_screen == "join_a_game":
            client_state.set_current_screen(JoinGame(client_state))
        if event.dest_screen == "game_list":
            client_state.set_current_screen(GameList(client_state))
        if event.dest_screen == "options":
            client_state.set_current_screen(Options(client_state))
        if event.dest_screen == "credits":
            client_state.set_current_screen(Credits(client_state))
        if event.dest_screen == "enter_name":
            client_state.set_current_screen(EnterName(client_state))
        if event.dest_screen == "profiles":
            client_state.set_current_screen(Profiles(client_state))


class ClearInternalGameInformationEventHandler(BaseEventHandler):
    def handle(self, event, client_state):
        client_state.profile.set_game(None)
        client_state.profile.set_game_event_pointer(None)


handlers_map = {
    ScreenTransitionEvent: ScreenTransitionEventHandler,
    ClearInternalGameInformationEvent: ClearInternalGameInformationEventHandler,
    InitiateGameEvent: InitiateGameEventHandler,
    # In game events, these events define the status of the game
    GameCreatedInGameEvent: GameCreatedInGameEventHandler,
    PlayerJoinedInGameEvent: PlayerJoinedInGameEventHandler,
    PlayerWinsInGameEvent: PlayerWinsInGameEventHandler,
}


class EventHandler:
    def handle(self, event, client_state):
        try:
            handlers_map[type(event)]().handle(event, client_state)
        except KeyError:
            pass  # Unhandled event
