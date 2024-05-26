from typing import Any, List, Optional

from client.engine.foundational_wrapper import FoundationalWrapper


class MouseInput:
    def read(self, events: List[any]) -> Optional[List[int]]:
        if FoundationalWrapper.MOUSEBUTTONDOWN in [event.type for event in events]:
            return "click"
        return None
