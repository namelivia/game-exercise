from typing import Any, Type

from engine.features.game_logic.worker import GameLogicWorker
from engine.features.network.worker import NetworkWorker
from engine.features.render.worker import RenderWorker
from engine.features.sound.worker import SoundWorker
from engine.features.user_input.worker import UserInputWorker
from engine.queue import QueueManager


class ThreadManager:
    _instance = None

    def __new__(
        cls: Type["ThreadManager"], *args: Any, **kwargs: Any
    ) -> "ThreadManager":
        if not cls._instance:
            cls._instance = super(ThreadManager, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:

        self.threads = [
            RenderWorker(
                name="Render",
                queue=QueueManager().get("render"),
            ),
            SoundWorker(
                name="Sound",
                queue=QueueManager().get("sound"),
            ),
            GameLogicWorker(
                name="Game Logic",
                queue=QueueManager().get("game_logic"),
            ),
            UserInputWorker(
                name="UserInput",
                queue=QueueManager().get("user_input"),
            ),
            NetworkWorker(
                name="Network",
                queue=QueueManager().get("network"),
            ),
        ]
        for thread in self.threads:
            thread.start()

    def shutdown(self) -> None:
        for thread in self.threads:
            thread.stop()
            thread.join()
