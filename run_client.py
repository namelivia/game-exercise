import logging

from client.engine.screen_manager import ScreenManagerFactory
from client.game.event_handler import EventHandler as GameEventHandler
from client.game.events import ScreenTransitionEvent

"""
This initializes the client
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="client_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    screen_manager = ScreenManagerFactory.create(
        initial_event=ScreenTransitionEvent("intro"), event_handler=GameEventHandler()
    )
    while True:
        screen_manager.run()
