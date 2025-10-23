import logging

from client.animation.event_handler import EventHandler as GameEventHandler
from client.animation.events import ScreenTransitionEvent
from client.engine.screen_manager import ScreenManagerFactory

"""
This initializes the animation
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="animation_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    screen_manager = ScreenManagerFactory.create(
        initial_event=ScreenTransitionEvent("main"),
        game_event_handler=GameEventHandler(),
    )
    while True:
        screen_manager.run()
