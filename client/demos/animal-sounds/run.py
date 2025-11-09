import logging

from animal_sounds.screens.main.main import MainScreen
from engine.api import start_application

"""
This initializes the animal_sounds
"""

if __name__ == "__main__":
    logging.basicConfig(
        filename="data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    start_application(initial_screen=MainScreen)
