from engine.features.sound.commands import PlaySound
from engine.features.sound.worker import SoundWorker
from engine.queue import QueueManager

if __name__ == "__main__":
    QueueManager().initialize()
    sound_thread = SoundWorker(
        name="Sound",
        queue=QueueManager().get("sound"),
    )

    sound_thread.start()
    PlaySound("sounds/elephant.mp3").execute()
