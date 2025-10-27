import time
from typing import Any, Optional, Type


class Clock:
    _instance: Optional["Clock"] = None

    _program_start_time: float
    _last_tick_time: float

    def __new__(cls: Type["Clock"], *args: Any, **kwargs: Any) -> "Clock":
        if not cls._instance:
            cls._instance = super(Clock, cls).__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        self._program_start_time = time.monotonic()
        self._last_tick_time = time.perf_counter()

    def tick(self, framerate: int = 0) -> int:
        current_time: float = time.perf_counter()
        elapsed_seconds: float = current_time - self._last_tick_time

        # Frame Rate Capping (The Pygame Clock purpose)
        if framerate > 0:
            target_frame_time: float = 1.0 / framerate
            delay_needed: float = target_frame_time - elapsed_seconds

            if delay_needed > 0:
                time.sleep(delay_needed)
                current_time = time.perf_counter()
                elapsed_seconds = current_time - self._last_tick_time

        # Update and return delta time in milliseconds
        self._last_tick_time = current_time
        return int(elapsed_seconds * 1000)

    def get_ticks(self) -> int:
        """
        Returns the total number of milliseconds since the clock was initialized.
        """
        elapsed_seconds: float = time.monotonic() - self._program_start_time
        return int(elapsed_seconds * 1000)
