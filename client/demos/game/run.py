import logging

from engine.api import start_application

from game.screens.intro.intro import Intro
from game.state import State

"""
This initializes the client
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="game_data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    State().initialize()

    start_application(
        initial_screen=Intro,
    )
