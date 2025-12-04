import logging

from engine.api import start_application
from labyrinth.screen_loader import load_screen
from labyrinth.screens.main.main import MainScreen

if __name__ == "__main__":
    logging.basicConfig(
        filename="data/logs/client.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(message)s",
    )

    screen = load_screen("labyrinth/screens/main/scene.json")
    print(screen.__dict__)
    exit()
    start_application(initial_screen=MainScreen)
