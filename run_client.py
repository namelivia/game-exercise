from client.engine.screen_manager import ScreenManager
from client.engine.input.input import Input
from client.engine.general_state.client_state import ClientState
from client.engine.graphics.graphics import Graphics

from client.game.events import ScreenTransitionEvent

USES_PYGAME = True

"""
This initializes the client
"""

if __name__ == "__main__":

    # The initial event is game specific
    initial_event = ScreenTransitionEvent("intro")
    client_state = ClientState(initial_event, "profile2")

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
