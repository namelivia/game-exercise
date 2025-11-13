import logging
from queue import Empty, SimpleQueue
from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from engine.primitives.event import Event

logger = logging.getLogger(__name__)


class QueueManager:
    _instance = None

    def __new__(cls: Type["QueueManager"], *args: Any, **kwargs: Any) -> "QueueManager":
        if not cls._instance:
            cls._instance = super(QueueManager, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        sound_queue = _Queue()
        sound_queue.initialize()
        game_logic_queue = _Queue()
        game_logic_queue.initialize()
        network_queue = _Queue()
        network_queue.initialize()
        render_queue = _Queue()
        render_queue.initialize()
        user_input_queue = _Queue()
        user_input_queue.initialize()
        self.queues = {
            "sound": sound_queue,
            "game_logic": game_logic_queue,
            "network": network_queue,
            "render": render_queue,
            "user_input": user_input_queue,
        }

    def get(self, key) -> "_Queue":
        return self.queues[key]


class _Queue:
    def initialize(self) -> None:
        self.simple_queue: SimpleQueue["Event"] = SimpleQueue()

    def put(self, new_event: "Event") -> None:
        self.simple_queue.put(new_event)

    def empty(self) -> bool:
        return self.simple_queue.empty()

    def get(self, timeout: Optional[float] = None) -> Optional["Event"]:
        event = self.simple_queue.get(block=True, timeout=timeout)
        logger.info(f"[Event] {event.__class__.__name__}")
        return event
