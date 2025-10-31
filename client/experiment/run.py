import logging

from engine.screen_manager import ScreenManagerFactory
from experiment.event_handler import EventHandler as GameEventHandler
from experiment.events import ScreenTransitionEvent

"""
This initializes the experiment
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="experiment_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    screen_manager = ScreenManagerFactory.create(
        initial_event=ScreenTransitionEvent("main"),
        game_event_handler=GameEventHandler(),
    )
    while True:
        screen_manager.run()
