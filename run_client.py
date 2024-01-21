import logging

from client.engine.general_state.client_state import ClientState
from client.engine.graphics.graphics import Graphics
from client.engine.input.keyboard import KeyboardInput
from client.engine.input.mouse import MouseInput
from client.engine.screen_manager import ScreenManager
from client.game.event_handler import EventHandler as GameEventHandler
from client.game.events import ScreenTransitionEvent

USES_PYGAME = True

"""
This initializes the client
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="client_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    # The initial event is game specific
    initial_event = ScreenTransitionEvent("intro")
    client_state = ClientState(initial_event, "Default profile")

    if USES_PYGAME:
        import pygame

        pygame.init()

    graphics = Graphics(USES_PYGAME)
    keyboard_input = KeyboardInput(USES_PYGAME)
    mouse_input = MouseInput(USES_PYGAME)

    screen_manager = ScreenManager(
        client_state, keyboard_input, mouse_input, graphics, GameEventHandler()
    )
    while True:
        screen_manager.run()
