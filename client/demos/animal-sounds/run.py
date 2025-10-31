import logging

from animal_sounds.event_handler import EventHandler as GameEventHandler
from animal_sounds.events import ScreenTransitionEvent
from engine.api import ApplicationFactory

"""
This initializes the animal_sounds
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    ApplicationFactory.create(
        initial_event=ScreenTransitionEvent("main"),
        game_event_handler=GameEventHandler(),
    ).run()
