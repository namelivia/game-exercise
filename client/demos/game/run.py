import logging

from engine.api import start_application

from game.event_handler import EventHandler as GameEventHandler
from game.events import ScreenTransitionEvent

"""
This initializes the client
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="game_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    start_application(
        initial_event=ScreenTransitionEvent("intro"),
        game_event_handler=GameEventHandler(),
    )
