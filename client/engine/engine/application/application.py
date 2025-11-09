import sys
import time

from engine.backend.backend import Backend
from engine.features.game_logic.state import State
from engine.threading.manager import ThreadManager


class Application:
    def run(self) -> None:
        while True:
            try:
                current_screen = State().get_current_screen()
                if current_screen is not None:
                    current_screen.update()
                time.sleep(0.01)

            except KeyboardInterrupt:
                ThreadManager().shutdown()
                Backend.quit()
                sys.exit()
