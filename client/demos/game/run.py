import logging

from engine.api import ApplicationFactory

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

    ApplicationFactory.create(
        initial_event=ScreenTransitionEvent("intro"),
        game_event_handler=GameEventHandler(),
    ).run()
