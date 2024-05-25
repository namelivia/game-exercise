import logging

import pygame

from client.engine.general_state.client_state import ClientState
from client.engine.graphics.graphics import Graphics
from client.engine.input.keyboard import KeyboardInput
from client.engine.input.mouse import MouseInput
from client.engine.screen_manager import ScreenManager
from client.experiment.event_handler import EventHandler as GameEventHandler
from client.experiment.events import ScreenTransitionEvent

"""
This initializes the experiment
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="experiment_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    pygame.init()
    graphics = Graphics()
    keyboard_input = KeyboardInput()
    mouse_input = MouseInput()
    client_state = ClientState(ScreenTransitionEvent("main"), "Default profile")

    # TODO: Move this to a factory

    screen_manager = ScreenManager(
        client_state, keyboard_input, mouse_input, graphics, GameEventHandler()
    )
    while True:
        screen_manager.run()
