from client.screen_manager import ScreenManager
from client.game_specific.events import ScreenTransitionEvent
from client.input.input import Input
from client.general_state.client_state import ClientState
from client.graphics.graphics import Graphics

USES_PYGAME = True

"""
This initializes the client
"""

if __name__ == "__main__":

    # The initial event is game specific
    initial_event = ScreenTransitionEvent("intro")
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
