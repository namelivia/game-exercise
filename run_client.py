from client.screen_manager import ScreenManager
from client.events import InitiateGameEvent
from client.input.input import Input
from client.general_state.client_state import ClientState
from client.graphics.graphics import Graphics
from client.game_data import GameData

from client.events import GameCreatedInGameEvent
from client.events import PlayerJoinedInGameEvent
from client.events import PlayerPlacedSymbolInGameEvent

USES_PYGAME = True

"""
This initializes the client
"""

if __name__ == "__main__":

    # The initial event is game specific
    # NOTE: I'm shortcutting the initial game event to do some tests, it should be:
    # initial_event = ScreenTransitionEvent("intro")
    initial_event = InitiateGameEvent(
        GameData(
            "test",
            "test",
            ["player_1", "player_2"],
            [
                GameCreatedInGameEvent("player_1"),
                PlayerJoinedInGameEvent("player_2"),
                PlayerPlacedSymbolInGameEvent("player_1", 0),
                PlayerPlacedSymbolInGameEvent("player_2", 1),
                PlayerPlacedSymbolInGameEvent("player_1", 3),
            ],
        )
    )
    client_state = ClientState(initial_event)

    # Only if using pygame
    input_manager = None
    if USES_PYGAME:
        import pygame

        pygame.init()
    graphics = Graphics(USES_PYGAME)
    input_manager = Input(USES_PYGAME)

    screen_manager = ScreenManager(client_state, input_manager, graphics)
    while True:
        screen_manager.run()
