import logging

from client.engine.general_state.client_state import ClientState
from client.engine.graphics.graphics import Graphics
from client.engine.input.input import Input
from client.engine.screen_manager import ScreenManager
from client.experiment.events import ScreenTransitionEvent

USES_PYGAME = True

"""
This initializes the experiment
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="experiment_data/logs/client.log",
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
    input_manager = Input(USES_PYGAME)

    screen_manager = ScreenManager(client_state, input_manager, graphics)
    while True:
        screen_manager.run()
