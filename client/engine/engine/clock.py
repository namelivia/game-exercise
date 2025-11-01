import time
from typing import Any, Type


class Clock:
    _instance = None

    def __new__(cls: Type["Clock"], *args: Any, **kwargs: Any) -> "Clock":
        if not cls._instance:
            cls._instance = super(Clock, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        self._program_start_time = time.monotonic()
        self._last_tick_time = time.perf_counter()

    def tick(self, framerate: int = 0) -> int:
        current_time = time.perf_counter()
        elapsed_seconds = current_time - self._last_tick_time

        # Frame rate capping
        if framerate > 0:
            target_frame_time = 1.0 / framerate
            delay_needed = target_frame_time - elapsed_seconds

            if delay_needed > 0:
                time.sleep(delay_needed)
                current_time = time.perf_counter()
                elapsed_seconds = current_time - self._last_tick_time

        # Update and return delta time in milliseconds
        self._last_tick_time = current_time
        return int(elapsed_seconds * 1000)

    def get_ticks(self) -> int:
        elapsed_seconds = time.monotonic() - self._program_start_time
        return int(elapsed_seconds * 1000)
