import pygame

from client.engine.features.user_input.worker import UserInputWorker
from client.engine.queue import QueueManager

if __name__ == "__main__":
    pygame.init()
    # A window must exists and must be focused for pygame to
    # capture input.
    screen = pygame.display.set_mode((1024, 768))
    QueueManager().initialize()
    user_input_thread = UserInputWorker(
        name="UserInput",
    )

    user_input_thread.start()
    while True:
        if not QueueManager().get("game_logic").empty():
            print(QueueManager().get("game_logic").get().__dict__)
