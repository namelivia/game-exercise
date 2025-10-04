import pygame

from client.engine.features.sound.commands import PlaySound
from client.engine.features.sound.worker import SoundWorker
from client.engine.general_state.options import Options
from client.engine.general_state.queue import QueueManager

if __name__ == "__main__":
    pygame.mixer.init()
    QueueManager().initialize()
    Options().initialize()
    sound_thread = SoundWorker(
        name="Sound",
        queue=QueueManager().get("sound"),
    )

    sound_thread.start()
    PlaySound("client/experiment/sounds/elephant.mp3").execute()
