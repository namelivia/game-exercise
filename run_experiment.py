import logging

import pygame

from client.engine.general_state.client_state import ClientState
from client.engine.screen_manager import ScreenManagerFactory
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
    screen_manager = ScreenManagerFactory.create(
        initial_event=ScreenTransitionEvent("main"), event_handler=GameEventHandler()
    )
    while True:
        screen_manager.run()
