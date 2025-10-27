import logging
from typing import (  # Added List and Union
    TYPE_CHECKING,
    Any,
    List,
    Optional,
    Type,
    Union,
)

from client.engine.features.game_logic.worker import GameLogicWorker
from client.engine.features.network.worker import NetworkWorker
from client.engine.features.render.worker import RenderWorker
from client.engine.features.sound.worker import SoundWorker
from client.engine.features.user_input.worker import UserInputWorker
from client.engine.general_state.queue import QueueManager
from client.engine.primitives.worker import Worker  # Assumed base class for all workers

if TYPE_CHECKING:
    from client.engine.primitives.event import Event

# Define a union type for all workers to simplify the 'threads' list hint
WorkerType = Union[
    RenderWorker,
    SoundWorker,
    GameLogicWorker,
    UserInputWorker,
    NetworkWorker,
    # Or just 'Worker' if all inherit from a common base class
]


logger = logging.getLogger(__name__)


class ThreadManager:
    # Singleton class attribute hint
    _instance: Optional["ThreadManager"] = None

    # Instance attribute hint, initialized in .initialize()
    # Using the Union type created above
    threads: List[WorkerType]

    # This class is a singleton
    def __new__(
        cls: Type["ThreadManager"], *args: Any, **kwargs: Any
    ) -> "ThreadManager":
        if not cls._instance:
            cls._instance = super(ThreadManager, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        """Initializes and starts all worker threads."""

        # Local variable with specific worker type for clarity
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

        # Local variable hint for the loop
        thread: WorkerType
        for thread in self.threads:
            thread.start()

    def shutdown(self) -> None:
        """Signals all worker threads to stop and waits for them to join."""

        # Local variable hint for the loop
        thread: WorkerType
        for thread in self.threads:
            thread.stop()
            thread.join()
