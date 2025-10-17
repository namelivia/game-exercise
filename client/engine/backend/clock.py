import time


class Clock:
    """
    Combines frame rate control (tick) and total runtime (get_ticks) functionality.
    """

    def __init__(self):
        # Time for total runtime tracking (simulates pygame.init())
        self._program_start_time = time.monotonic()

        # Time for frame rate tracking (simulates pygame.time.Clock())
        self._last_tick_time = time.perf_counter()

    def tick(self, framerate: int = 0) -> int:
        """
        Pauses the program to limit the framerate and returns the milliseconds
        elapsed since the last call (delta time).
        """
        current_time = time.perf_counter()
        elapsed_seconds = current_time - self._last_tick_time

        # Frame Rate Capping (The FoundationalClock purpose)
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
        """
        Returns the total number of milliseconds since the clock was initialized.
        (The FoundationalWrapper purpose)
        """
        elapsed_seconds = time.monotonic() - self._program_start_time
        return int(elapsed_seconds * 1000)


# Example Usage
# clock = GameClock()
# print(f"Time at start: {clock.get_ticks()} ms")
# # Game loop would look something like this:
# # while running:
# #     delta_time = clock.tick(60) # Limits to 60 FPS
# #     total_time = clock.get_ticks()
# #     # ... update game logic using delta_time ...
