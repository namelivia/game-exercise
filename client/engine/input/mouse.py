from typing import Any, List, Optional

from client.engine.external.foundational_wrapper import FoundationalWrapper


class MouseInput:
    def read(self, events: List[Any]) -> Optional[str]:
        if FoundationalWrapper.MOUSEBUTTONDOWN in [event.type for event in events]:
            return "click"
        return None
