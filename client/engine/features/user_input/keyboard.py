from typing import Any, List

from client.engine.backend.input import InputBackend


class KeyboardInput:
    def _get_key_value(self, event: Any) -> Any:
        special_keys = {
            InputBackend.K_RETURN: "return",
            InputBackend.K_ESCAPE: "escape",
            InputBackend.K_BACKSPACE: "backspace",
        }
        if event.key in special_keys:
            return special_keys[event.key]
        else:
            return event.unicode

    def read(self, events: List[Any]) -> List[str]:
        keydowns = [event for event in events if event.type == InputBackend.KEYDOWN]
        return [self._get_key_value(event) for event in keydowns]
