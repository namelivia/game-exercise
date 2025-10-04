from typing import Any, List, Optional

from client.engine.backend.input import InputBackend


class MouseInput:
    def read(self, events: List[Any]) -> Optional[str]:
        if InputBackend.MOUSEBUTTONDOWN in [event.type for event in events]:
            return "click"
        return None
