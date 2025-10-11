import logging
from typing import TYPE_CHECKING, Any, Optional, Type

from client.engine.features.game_logic.worker import GameLogicWorker
from client.engine.features.network.worker import NetworkWorker
from client.engine.features.render.worker import RenderWorker
from client.engine.features.sound.worker import SoundWorker
from client.engine.features.user_input.worker import UserInputWorker
from client.engine.general_state.queue import QueueManager

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

logger = logging.getLogger(__name__)


class ThreadManager:
    _instance = None

    # This class is a singleton
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
            UserInputWorker(name="UserInput"),
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
