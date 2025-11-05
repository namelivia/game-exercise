import sys
import time

from engine.backend.backend import Backend
from engine.current_screen import CurrentScreen
from engine.threading.manager import ThreadManager


class Application:
    def run(self) -> None:
        while True:
            try:
                current_screen = CurrentScreen().get_current_screen()
                if current_screen is not None:
                    current_screen.update()
                time.sleep(0.01)

            except KeyboardInterrupt:
                ThreadManager().shutdown()
                Backend.quit()
                sys.exit()
