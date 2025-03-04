from typing import Tuple

from client.engine.external.foundational_wrapper import FoundationalWrapper


class Mouse:
    def get(self) -> Tuple[int, int]:
        return FoundationalWrapper.get_mouse_position()
